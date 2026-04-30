"""
Gmail channel handler for email support.

This module handles:
- Gmail API integration
- Push notifications via Pub/Sub
- Email parsing and sending
- Thread management
"""

import os
import base64
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from email.mime.text import MIMEText

# Google API imports
try:
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build
    from google.auth.transport.requests import Request
    GOOGLE_AVAILABLE = True
except ImportError:
    GOOGLE_AVAILABLE = False
    logging.warning("Google API libraries not installed. Gmail integration disabled.")

logger = logging.getLogger(__name__)


class GmailHandler:
    """Handler for Gmail integration."""

    def __init__(self):
        if not GOOGLE_AVAILABLE:
            raise RuntimeError("Google API libraries not installed")

        self.credentials_path = os.getenv("GMAIL_CREDENTIALS_PATH", "./credentials/gmail_credentials.json")
        self.token_path = os.getenv("GMAIL_TOKEN_PATH", "./credentials/gmail_token.json")
        self.credentials = None
        self.service = None

    def _load_credentials(self):
        """Load Gmail API credentials."""
        if not os.path.exists(self.token_path):
            raise FileNotFoundError(
                f"Gmail token not found at {self.token_path}. "
                "Please run the OAuth flow to generate credentials."
            )

        self.credentials = Credentials.from_authorized_user_file(
            self.token_path,
            scopes=['https://www.googleapis.com/auth/gmail.modify']
        )

        # Refresh if expired
        if self.credentials.expired and self.credentials.refresh_token:
            self.credentials.refresh(Request())

        self.service = build('gmail', 'v1', credentials=self.credentials)
        logger.info("Gmail credentials loaded successfully")

    async def setup_push_notifications(self, topic_name: str):
        """
        Set up Gmail push notifications via Pub/Sub.

        Args:
            topic_name: Full Pub/Sub topic name (e.g., projects/PROJECT_ID/topics/gmail-notifications)
        """
        if not self.service:
            self._load_credentials()

        try:
            request = {
                'labelIds': ['INBOX'],
                'topicName': topic_name,
                'labelFilterAction': 'include'
            }
            result = self.service.users().watch(userId='me', body=request).execute()
            logger.info(f"Gmail push notifications enabled: {result}")
            return result
        except Exception as e:
            logger.error(f"Failed to setup push notifications: {e}")
            raise

    async def process_notification(self, pubsub_message: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Process incoming Pub/Sub notification from Gmail.

        Args:
            pubsub_message: Pub/Sub message data

        Returns:
            List of parsed email messages
        """
        if not self.service:
            self._load_credentials()

        try:
            history_id = pubsub_message.get('historyId')

            # Get new messages since last history ID
            history = self.service.users().history().list(
                userId='me',
                startHistoryId=history_id,
                historyTypes=['messageAdded']
            ).execute()

            messages = []
            for record in history.get('history', []):
                for msg_added in record.get('messagesAdded', []):
                    msg_id = msg_added['message']['id']
                    message = await self.get_message(msg_id)
                    messages.append(message)

            logger.info(f"Processed {len(messages)} new emails")
            return messages

        except Exception as e:
            logger.error(f"Failed to process notification: {e}")
            raise

    async def get_message(self, message_id: str) -> Dict[str, Any]:
        """
        Fetch and parse a Gmail message.

        Args:
            message_id: Gmail message ID

        Returns:
            Parsed message data
        """
        if not self.service:
            self._load_credentials()

        try:
            msg = self.service.users().messages().get(
                userId='me',
                id=message_id,
                format='full'
            ).execute()

            # Extract headers
            headers = {h['name']: h['value'] for h in msg['payload']['headers']}

            # Extract body
            body = self._extract_body(msg['payload'])

            return {
                'channel': 'email',
                'channel_message_id': message_id,
                'customer_email': self._extract_email(headers.get('From', '')),
                'customer_name': self._extract_name(headers.get('From', '')),
                'subject': headers.get('Subject', ''),
                'content': body,
                'received_at': datetime.utcnow().isoformat(),
                'thread_id': msg.get('threadId'),
                'metadata': {
                    'headers': headers,
                    'labels': msg.get('labelIds', [])
                }
            }

        except Exception as e:
            logger.error(f"Failed to get message {message_id}: {e}")
            raise

    def _extract_body(self, payload: Dict[str, Any]) -> str:
        """Extract text body from email payload."""
        # Check for direct body
        if 'body' in payload and payload['body'].get('data'):
            return base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8')

        # Check for parts (multipart)
        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    if 'data' in part['body']:
                        return base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                # Recursively check nested parts
                if 'parts' in part:
                    body = self._extract_body(part)
                    if body:
                        return body

        return ''

    def _extract_email(self, from_header: str) -> str:
        """Extract email address from From header."""
        import re
        match = re.search(r'<(.+?)>', from_header)
        return match.group(1) if match else from_header.strip()

    def _extract_name(self, from_header: str) -> str:
        """Extract name from From header."""
        import re
        # Try to extract name before email
        match = re.match(r'^(.+?)\s*<.+?>$', from_header)
        if match:
            return match.group(1).strip().strip('"')
        return ''

    async def send_reply(
        self,
        to_email: str,
        subject: str,
        body: str,
        thread_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Send email reply.

        Args:
            to_email: Recipient email address
            subject: Email subject
            body: Email body (plain text)
            thread_id: Optional thread ID to reply in thread

        Returns:
            Send result with message ID
        """
        if not self.service:
            self._load_credentials()

        try:
            # Create message
            message = MIMEText(body)
            message['to'] = to_email
            message['subject'] = f"Re: {subject}" if not subject.startswith('Re:') else subject

            # Encode message
            raw = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')

            # Prepare send request
            send_request = {'raw': raw}
            if thread_id:
                send_request['threadId'] = thread_id

            # Send
            result = self.service.users().messages().send(
                userId='me',
                body=send_request
            ).execute()

            logger.info(f"Email sent: {result['id']}")

            return {
                'channel_message_id': result['id'],
                'delivery_status': 'sent',
                'thread_id': result.get('threadId')
            }

        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            raise


# Singleton instance
_gmail_handler = None


def get_gmail_handler() -> GmailHandler:
    """Get or create the Gmail handler instance."""
    global _gmail_handler

    if _gmail_handler is None:
        if os.getenv("GMAIL_ENABLED", "false") == "true":
            _gmail_handler = GmailHandler()
        else:
            raise RuntimeError("Gmail integration is not enabled")

    return _gmail_handler

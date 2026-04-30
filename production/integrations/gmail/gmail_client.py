"""
Gmail Integration Client
Handles OAuth2 authentication and email operations
"""
import os
import base64
from typing import List, Dict, Optional
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pickle

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

class GmailClient:
    def __init__(self, credentials_path: str = "credentials/gmail_credentials.json"):
        self.credentials_path = credentials_path
        self.token_path = "credentials/gmail_token.pickle"
        self.service = None

    def authenticate(self) -> bool:
        """Authenticate with Gmail API using OAuth2"""
        creds = None

        # Load existing token
        if os.path.exists(self.token_path):
            with open(self.token_path, 'rb') as token:
                creds = pickle.load(token)

        # Refresh or get new credentials
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, SCOPES)
                creds = flow.run_local_server(port=0)

            # Save credentials
            with open(self.token_path, 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('gmail', 'v1', credentials=creds)
        return True

    def get_unread_messages(self, max_results: int = 10) -> List[Dict]:
        """Get unread messages from inbox"""
        try:
            results = self.service.users().messages().list(
                userId='me',
                labelIds=['INBOX', 'UNREAD'],
                maxResults=max_results
            ).execute()

            messages = results.get('messages', [])
            detailed_messages = []

            for msg in messages:
                msg_data = self.service.users().messages().get(
                    userId='me',
                    id=msg['id'],
                    format='full'
                ).execute()

                detailed_messages.append(self._parse_message(msg_data))

            return detailed_messages

        except HttpError as error:
            print(f'Gmail API error: {error}')
            return []

    def _parse_message(self, msg_data: Dict) -> Dict:
        """Parse Gmail message data"""
        headers = msg_data['payload']['headers']

        # Extract headers
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
        sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown')
        date = next((h['value'] for h in headers if h['name'] == 'Date'), '')

        # Extract body
        body = self._get_message_body(msg_data['payload'])

        return {
            'id': msg_data['id'],
            'thread_id': msg_data['threadId'],
            'subject': subject,
            'from': sender,
            'date': date,
            'body': body,
            'snippet': msg_data.get('snippet', '')
        }

    def _get_message_body(self, payload: Dict) -> str:
        """Extract message body from payload"""
        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    data = part['body'].get('data', '')
                    if data:
                        return base64.urlsafe_b64decode(data).decode('utf-8')
        elif 'body' in payload:
            data = payload['body'].get('data', '')
            if data:
                return base64.urlsafe_b64decode(data).decode('utf-8')

        return ''

    def send_reply(self, to: str, subject: str, body: str, thread_id: Optional[str] = None) -> bool:
        """Send email reply"""
        try:
            message = MIMEText(body)
            message['to'] = to
            message['subject'] = f"Re: {subject}" if not subject.startswith('Re:') else subject

            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')

            send_message = {'raw': raw_message}
            if thread_id:
                send_message['threadId'] = thread_id

            self.service.users().messages().send(
                userId='me',
                body=send_message
            ).execute()

            return True

        except HttpError as error:
            print(f'Error sending email: {error}')
            return False

    def mark_as_read(self, message_id: str) -> bool:
        """Mark message as read"""
        try:
            self.service.users().messages().modify(
                userId='me',
                id=message_id,
                body={'removeLabelIds': ['UNREAD']}
            ).execute()
            return True
        except HttpError as error:
            print(f'Error marking as read: {error}')
            return False

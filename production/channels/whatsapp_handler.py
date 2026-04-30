"""
WhatsApp channel handler via Twilio.

This module handles:
- Twilio WhatsApp API integration
- Webhook validation
- Message parsing and sending
- Status callbacks
"""

import os
import logging
from typing import Dict, Any, Optional
from datetime import datetime

try:
    from twilio.rest import Client
    from twilio.request_validator import RequestValidator
    TWILIO_AVAILABLE = True
except ImportError:
    TWILIO_AVAILABLE = False
    logging.warning("Twilio library not installed. WhatsApp integration disabled.")

from fastapi import Request, HTTPException

logger = logging.getLogger(__name__)


class WhatsAppHandler:
    """Handler for WhatsApp integration via Twilio."""

    def __init__(self):
        if not TWILIO_AVAILABLE:
            raise RuntimeError("Twilio library not installed")

        self.account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        self.auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.whatsapp_number = os.getenv('TWILIO_WHATSAPP_NUMBER')

        if not all([self.account_sid, self.auth_token, self.whatsapp_number]):
            raise ValueError("Missing Twilio credentials in environment variables")

        self.client = Client(self.account_sid, self.auth_token)
        self.validator = RequestValidator(self.auth_token)

        logger.info(f"WhatsApp handler initialized: {self.whatsapp_number}")

    async def validate_webhook(self, request: Request) -> bool:
        """
        Validate incoming Twilio webhook signature.

        Args:
            request: FastAPI request object

        Returns:
            True if signature is valid
        """
        try:
            signature = request.headers.get('X-Twilio-Signature', '')
            url = str(request.url)
            form_data = await request.form()
            params = dict(form_data)

            is_valid = self.validator.validate(url, params, signature)

            if not is_valid:
                logger.warning(f"Invalid Twilio signature from {request.client.host}")

            return is_valid

        except Exception as e:
            logger.error(f"Error validating webhook: {e}")
            return False

    async def process_webhook(self, form_data: Dict[str, str]) -> Dict[str, Any]:
        """
        Process incoming WhatsApp message from Twilio webhook.

        Args:
            form_data: Form data from Twilio webhook

        Returns:
            Parsed message data
        """
        try:
            # Extract phone number (remove 'whatsapp:' prefix)
            from_number = form_data.get('From', '').replace('whatsapp:', '')

            message_data = {
                'channel': 'whatsapp',
                'channel_message_id': form_data.get('MessageSid'),
                'customer_phone': from_number,
                'customer_name': form_data.get('ProfileName', ''),
                'content': form_data.get('Body', ''),
                'received_at': datetime.utcnow().isoformat(),
                'metadata': {
                    'num_media': int(form_data.get('NumMedia', '0')),
                    'wa_id': form_data.get('WaId'),
                    'status': form_data.get('SmsStatus'),
                    'from_city': form_data.get('FromCity'),
                    'from_state': form_data.get('FromState'),
                    'from_country': form_data.get('FromCountry')
                }
            }

            # Handle media attachments if present
            num_media = int(form_data.get('NumMedia', '0'))
            if num_media > 0:
                media_urls = []
                for i in range(num_media):
                    media_url = form_data.get(f'MediaUrl{i}')
                    media_type = form_data.get(f'MediaContentType{i}')
                    if media_url:
                        media_urls.append({
                            'url': media_url,
                            'type': media_type
                        })
                message_data['metadata']['media'] = media_urls

            logger.info(f"WhatsApp message received from {from_number}")
            return message_data

        except Exception as e:
            logger.error(f"Error processing WhatsApp webhook: {e}")
            raise

    async def send_message(self, to_phone: str, body: str) -> Dict[str, Any]:
        """
        Send WhatsApp message via Twilio.

        Args:
            to_phone: Recipient phone number
            body: Message body

        Returns:
            Send result with message SID and status
        """
        try:
            # Ensure phone number is in WhatsApp format
            if not to_phone.startswith('whatsapp:'):
                to_phone = f'whatsapp:{to_phone}'

            # Send message
            message = self.client.messages.create(
                body=body,
                from_=self.whatsapp_number,
                to=to_phone
            )

            logger.info(f"WhatsApp message sent: {message.sid}")

            return {
                'channel_message_id': message.sid,
                'delivery_status': message.status,  # queued, sent, delivered, failed
                'to': to_phone,
                'sent_at': datetime.utcnow().isoformat()
            }

        except Exception as e:
            logger.error(f"Failed to send WhatsApp message: {e}")
            raise

    def format_response(self, response: str, max_length: int = 1600) -> list:
        """
        Format and split response for WhatsApp (max 1600 chars per message).

        Args:
            response: Response text
            max_length: Maximum characters per message

        Returns:
            List of message chunks
        """
        if len(response) <= max_length:
            return [response]

        # Split into multiple messages
        messages = []
        remaining = response

        while remaining:
            if len(remaining) <= max_length:
                messages.append(remaining)
                break

            # Find a good break point (sentence or word boundary)
            break_point = remaining.rfind('. ', 0, max_length)
            if break_point == -1:
                break_point = remaining.rfind(' ', 0, max_length)
            if break_point == -1:
                break_point = max_length

            chunk = remaining[:break_point + 1].strip()
            messages.append(chunk)
            remaining = remaining[break_point + 1:].strip()

        logger.info(f"Split response into {len(messages)} WhatsApp messages")
        return messages

    async def send_multiple_messages(self, to_phone: str, messages: list) -> list:
        """
        Send multiple WhatsApp messages in sequence.

        Args:
            to_phone: Recipient phone number
            messages: List of message bodies

        Returns:
            List of send results
        """
        results = []

        for i, message in enumerate(messages):
            try:
                result = await self.send_message(to_phone, message)
                results.append(result)

                # Small delay between messages to avoid rate limiting
                if i < len(messages) - 1:
                    import asyncio
                    await asyncio.sleep(0.5)

            except Exception as e:
                logger.error(f"Failed to send message {i+1}/{len(messages)}: {e}")
                results.append({
                    'error': str(e),
                    'delivery_status': 'failed'
                })

        return results

    async def update_delivery_status(
        self,
        message_sid: str,
        status: str
    ) -> None:
        """
        Update message delivery status in database.

        Args:
            message_sid: Twilio message SID
            status: New status (queued, sent, delivered, read, failed)
        """
        try:
            # TODO: Update in database
            logger.info(f"Message {message_sid} status: {status}")

        except Exception as e:
            logger.error(f"Failed to update delivery status: {e}")


# Singleton instance
_whatsapp_handler = None


def get_whatsapp_handler() -> WhatsAppHandler:
    """Get or create the WhatsApp handler instance."""
    global _whatsapp_handler

    if _whatsapp_handler is None:
        if os.getenv("WHATSAPP_ENABLED", "false") == "true":
            _whatsapp_handler = WhatsAppHandler()
        else:
            raise RuntimeError("WhatsApp integration is not enabled")

    return _whatsapp_handler

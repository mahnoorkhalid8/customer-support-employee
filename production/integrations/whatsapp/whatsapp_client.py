"""
WhatsApp Integration via Twilio
Handles sending and receiving WhatsApp messages
"""
import os
from typing import Dict, Optional
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

class WhatsAppClient:
    def __init__(self):
        self.account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        self.auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        self.whatsapp_number = os.getenv("TWILIO_WHATSAPP_NUMBER")

        if not all([self.account_sid, self.auth_token, self.whatsapp_number]):
            raise ValueError("Missing Twilio credentials in environment variables")

        self.client = Client(self.account_sid, self.auth_token)

    def send_message(self, to: str, body: str) -> Dict:
        """
        Send WhatsApp message

        Args:
            to: Recipient phone number (format: +1234567890)
            body: Message text

        Returns:
            Dict with status and message_sid
        """
        try:
            # Ensure 'whatsapp:' prefix
            if not to.startswith('whatsapp:'):
                to = f'whatsapp:{to}'

            if not self.whatsapp_number.startswith('whatsapp:'):
                from_number = f'whatsapp:{self.whatsapp_number}'
            else:
                from_number = self.whatsapp_number

            message = self.client.messages.create(
                body=body,
                from_=from_number,
                to=to
            )

            return {
                'success': True,
                'message_sid': message.sid,
                'status': message.status
            }

        except TwilioRestException as e:
            return {
                'success': False,
                'error': str(e),
                'error_code': e.code
            }

    def parse_incoming_message(self, form_data: Dict) -> Dict:
        """
        Parse incoming WhatsApp webhook data from Twilio

        Args:
            form_data: Form data from Twilio webhook

        Returns:
            Parsed message data
        """
        return {
            'message_sid': form_data.get('MessageSid'),
            'from': form_data.get('From', '').replace('whatsapp:', ''),
            'to': form_data.get('To', '').replace('whatsapp:', ''),
            'body': form_data.get('Body', ''),
            'num_media': int(form_data.get('NumMedia', 0)),
            'profile_name': form_data.get('ProfileName', ''),
            'timestamp': form_data.get('Timestamp')
        }

    def validate_webhook(self, request_url: str, params: Dict, signature: str) -> bool:
        """
        Validate Twilio webhook signature

        Args:
            request_url: Full URL of the webhook
            params: Request parameters
            signature: X-Twilio-Signature header

        Returns:
            True if signature is valid
        """
        from twilio.request_validator import RequestValidator

        validator = RequestValidator(self.auth_token)
        return validator.validate(request_url, params, signature)

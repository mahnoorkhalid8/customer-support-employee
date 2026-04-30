"""
Customer Support AI Service
Handles AI-powered responses for customer support across channels
"""
import os
from typing import List, Dict, Optional

class CustomerSupportAI:
    def __init__(self):
        # Determine which AI provider to use
        self.provider = os.getenv("AI_PROVIDER", "grok").lower()

        if self.provider == "gemini":
            from production.gemini_client import get_gemini_client, get_model_name
            self.client = get_gemini_client()
            self.model = get_model_name()
        else:
            from production.grok_client import get_grok_client, get_model_name
            self.client = get_grok_client()
            self.model = get_model_name()

    def generate_response(
        self,
        customer_message: str,
        channel: str = "email",
        context: Optional[Dict] = None,
        conversation_history: Optional[List[Dict]] = None
    ) -> str:
        """
        Generate customer support response

        Args:
            customer_message: Customer's message
            channel: Communication channel (email, whatsapp, web)
            context: Additional context (customer info, previous issues, etc.)
            conversation_history: Previous messages in conversation

        Returns:
            AI-generated response
        """
        # Build system prompt based on channel
        system_prompt = self._get_system_prompt(channel)

        # Generate response based on provider
        try:
            if self.provider == "gemini":
                # Gemini API (new google.genai package)
                prompt_parts = [system_prompt]

                # Add context
                if context:
                    context_str = self._format_context(context)
                    prompt_parts.append(f"Additional context: {context_str}")

                # Add conversation history
                if conversation_history:
                    for msg in conversation_history:
                        prompt_parts.append(f"{msg['role']}: {msg['content']}")

                # Add current message
                prompt_parts.append(f"User: {customer_message}")
                prompt_parts.append("Assistant:")

                full_prompt = "\n\n".join(prompt_parts)

                # Use the new API
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=full_prompt
                )
                return response.text

            else:
                # OpenAI/Grok API
                messages = [{"role": "system", "content": system_prompt}]

                # Add conversation history
                if conversation_history:
                    messages.extend(conversation_history)

                # Add context
                if context:
                    context_str = self._format_context(context)
                    messages.append({
                        "role": "system",
                        "content": f"Additional context: {context_str}"
                    })

                # Add current message
                messages.append({
                    "role": "user",
                    "content": customer_message
                })

                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=0.7,
                    max_tokens=500 if channel == "whatsapp" else 1000
                )

                return response.choices[0].message.content

        except Exception as e:
            print(f"AI generation error: {e}")
            return self._get_fallback_response(channel)

    def _get_system_prompt(self, channel: str) -> str:
        """Get system prompt based on channel"""
        base_prompt = """You are a helpful customer support AI assistant. Your role is to:
- Provide accurate, helpful, and professional responses
- Be empathetic and understanding
- Solve customer problems efficiently
- Escalate to human agents when necessary
- Keep responses clear and actionable

Always maintain a friendly, professional tone."""

        if channel == "whatsapp":
            return base_prompt + "\n\nIMPORTANT: Keep responses brief and conversational for WhatsApp. Use short paragraphs."
        elif channel == "email":
            return base_prompt + "\n\nIMPORTANT: Provide detailed, well-structured email responses with proper formatting."
        else:
            return base_prompt

    def _format_context(self, context: Dict) -> str:
        """Format context dictionary into readable string"""
        parts = []
        if context.get("customer_name"):
            parts.append(f"Customer: {context['customer_name']}")
        if context.get("customer_email"):
            parts.append(f"Email: {context['customer_email']}")
        if context.get("previous_issues"):
            parts.append(f"Previous issues: {context['previous_issues']}")
        if context.get("account_status"):
            parts.append(f"Account status: {context['account_status']}")

        return " | ".join(parts)

    def _get_fallback_response(self, channel: str) -> str:
        """Get fallback response when AI fails"""
        if channel == "whatsapp":
            return "Sorry, I'm having trouble right now. A team member will help you shortly! 🙏"
        else:
            return "I apologize, but I'm experiencing technical difficulties. A human agent will assist you shortly."

    def generate_email_response(
        self,
        subject: str,
        body: str,
        sender: str,
        sender_name: Optional[str] = None
    ) -> Dict[str, str]:
        """Generate email response"""
        context = {
            "customer_email": sender,
            "customer_name": sender_name or sender.split("@")[0]
        }

        prompt = f"""Subject: {subject}

From: {sender}

Message:
{body}

Please provide a helpful, professional email response."""

        response_body = self.generate_response(
            customer_message=prompt,
            channel="email",
            context=context
        )

        return {
            "subject": f"Re: {subject}" if not subject.startswith("Re:") else subject,
            "body": response_body
        }

    def generate_whatsapp_response(
        self,
        message: str,
        sender: str,
        sender_name: Optional[str] = None
    ) -> str:
        """Generate WhatsApp response"""
        context = {
            "customer_name": sender_name or "Customer",
            "customer_phone": sender
        }

        return self.generate_response(
            customer_message=message,
            channel="whatsapp",
            context=context
        )

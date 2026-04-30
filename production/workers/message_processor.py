"""
Message Processor Worker

This worker:
1. Consumes messages from Kafka (all channels)
2. Processes them through the AI agent
3. Stores results in database
4. Publishes metrics
"""

import asyncio
import logging
import os
import sys
from datetime import datetime
from typing import Dict, Any

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from production.kafka_client import FTEKafkaConsumer, FTEKafkaProducer, TOPICS
from production.database.queries import (
    init_db_pool,
    close_db_pool,
    get_customer_by_email,
    get_customer_by_phone,
    create_customer,
    create_conversation,
    get_active_conversation,
    store_message,
    record_metric
)
from production.agent.formatters import Channel

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class UnifiedMessageProcessor:
    """Process incoming messages from all channels through the FTE agent."""

    def __init__(self):
        self.producer = FTEKafkaProducer()
        self.consumer = None

    async def start(self):
        """Start the message processor."""
        logger.info("Starting Unified Message Processor...")

        # Initialize database
        await init_db_pool()
        logger.info("Database pool initialized")

        # Start Kafka producer
        await self.producer.start()
        logger.info("Kafka producer started")

        # Create Kafka consumer
        self.consumer = FTEKafkaConsumer(
            topics=[TOPICS['tickets_incoming']],
            group_id=os.getenv("KAFKA_CONSUMER_GROUP_ID", "fte-message-processor")
        )
        await self.consumer.start()
        logger.info("Kafka consumer started")

        # Start consuming messages
        logger.info("Message processor ready. Listening for tickets...")
        await self.consumer.consume(self.process_message)

    async def stop(self):
        """Stop the message processor."""
        logger.info("Stopping message processor...")

        if self.consumer:
            await self.consumer.stop()

        await self.producer.stop()
        await close_db_pool()

        logger.info("Message processor stopped")

    async def process_message(self, topic: str, message: Dict[str, Any]):
        """
        Process a single incoming message from any channel.

        Args:
            topic: Kafka topic name
            message: Message data
        """
        start_time = datetime.utcnow()

        try:
            logger.info(f"Processing message from {message.get('channel')}: {message.get('channel_message_id')}")

            # Extract channel
            channel = Channel(message['channel'])

            # Step 1: Resolve or create customer
            customer_id = await self.resolve_customer(message)
            logger.info(f"Customer resolved: {customer_id}")

            # Step 2: Get or create conversation
            conversation_id = await self.get_or_create_conversation(
                customer_id=customer_id,
                channel=channel,
                message=message
            )
            logger.info(f"Conversation: {conversation_id}")

            # Step 3: Store incoming message
            await store_message(
                conversation_id=conversation_id,
                channel=channel.value,
                direction='inbound',
                role='customer',
                content=message['content'],
                channel_message_id=message.get('channel_message_id')
            )

            # Step 4: Load conversation history
            # TODO: Implement conversation history loading
            history = []

            # Step 5: Run agent
            # TODO: Implement actual agent execution with OpenAI Agents SDK
            # For now, generate a placeholder response
            agent_response = await self.run_agent_placeholder(
                customer_id=customer_id,
                conversation_id=conversation_id,
                channel=channel,
                message=message,
                history=history
            )

            # Step 6: Store agent response
            await store_message(
                conversation_id=conversation_id,
                channel=channel.value,
                direction='outbound',
                role='agent',
                content=agent_response['output'],
                tokens_used=agent_response.get('tokens_used'),
                latency_ms=agent_response.get('latency_ms')
            )

            # Step 7: Calculate and publish metrics
            latency_ms = (datetime.utcnow() - start_time).total_seconds() * 1000

            await self.producer.publish(TOPICS['metrics'], {
                'event_type': 'message_processed',
                'channel': channel.value,
                'latency_ms': latency_ms,
                'customer_id': customer_id,
                'conversation_id': conversation_id
            })

            await record_metric(
                metric_name='message_processed',
                metric_value=1,
                channel=channel.value,
                dimensions={'conversation_id': conversation_id}
            )

            logger.info(f"Message processed successfully in {latency_ms:.0f}ms")

        except Exception as e:
            logger.error(f"Error processing message: {e}", exc_info=True)
            await self.handle_error(message, e)

    async def resolve_customer(self, message: Dict[str, Any]) -> str:
        """
        Resolve or create customer from message identifiers.

        Args:
            message: Message data

        Returns:
            Customer ID
        """
        # Try to find by email first
        if email := message.get('customer_email'):
            customer = await get_customer_by_email(email)
            if customer:
                return str(customer['id'])

            # Create new customer
            customer_id = await create_customer(
                email=email,
                name=message.get('customer_name', '')
            )
            return customer_id

        # Try phone for WhatsApp
        if phone := message.get('customer_phone'):
            customer = await get_customer_by_phone(phone)
            if customer:
                return str(customer['id'])

            # Create new customer with phone
            customer_id = await create_customer(
                phone=phone,
                name=message.get('customer_name', '')
            )
            return customer_id

        raise ValueError("Could not resolve customer from message")

    async def get_or_create_conversation(
        self,
        customer_id: str,
        channel: Channel,
        message: Dict[str, Any]
    ) -> str:
        """
        Get active conversation or create new one.

        Args:
            customer_id: Customer ID
            channel: Communication channel
            message: Message data

        Returns:
            Conversation ID
        """
        # Check for active conversation (within last 24 hours)
        active = await get_active_conversation(customer_id)

        if active:
            return str(active['id'])

        # Create new conversation
        conversation_id = await create_conversation(
            customer_id=customer_id,
            channel=channel.value
        )

        return conversation_id

    async def run_agent_placeholder(
        self,
        customer_id: str,
        conversation_id: str,
        channel: Channel,
        message: Dict[str, Any],
        history: list
    ) -> Dict[str, Any]:
        """
        Placeholder for agent execution.

        TODO: Replace with actual OpenAI Agents SDK implementation.

        Args:
            customer_id: Customer ID
            conversation_id: Conversation ID
            channel: Communication channel
            message: Message data
            history: Conversation history

        Returns:
            Agent response
        """
        # Simulate agent processing
        await asyncio.sleep(0.5)

        # Generate placeholder response
        response = f"Thank you for contacting TechCorp Support. I've received your message: '{message['content'][:50]}...'. Our AI agent will process this shortly."

        return {
            'output': response,
            'tokens_used': 100,
            'latency_ms': 500,
            'escalated': False
        }

    async def handle_error(self, message: Dict[str, Any], error: Exception):
        """
        Handle processing errors gracefully.

        Args:
            message: Original message
            error: Exception that occurred
        """
        logger.error(f"Handling error for message: {message.get('channel_message_id')}")

        # TODO: Send apologetic response via appropriate channel

        # Publish to DLQ
        await self.producer.publish(TOPICS['dlq'], {
            'event_type': 'processing_error',
            'original_message': message,
            'error': str(error),
            'error_type': type(error).__name__,
            'requires_human': True
        })


async def main():
    """Main entry point for the worker."""
    processor = UnifiedMessageProcessor()

    try:
        await processor.start()
    except KeyboardInterrupt:
        logger.info("Received shutdown signal")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
    finally:
        await processor.stop()


if __name__ == "__main__":
    asyncio.run(main())

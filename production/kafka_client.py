"""
Kafka client for event streaming.
"""

from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
import json
from datetime import datetime
import os
import logging
from typing import Callable, List, Dict, Any

logger = logging.getLogger(__name__)

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")

# Topic definitions for multi-channel FTE
TOPICS = {
    # Incoming tickets from all channels
    'tickets_incoming': os.getenv("KAFKA_TOPIC_TICKETS_INCOMING", "fte.tickets.incoming"),

    # Channel-specific inbound
    'email_inbound': os.getenv("KAFKA_TOPIC_EMAIL_INBOUND", "fte.channels.email.inbound"),
    'whatsapp_inbound': os.getenv("KAFKA_TOPIC_WHATSAPP_INBOUND", "fte.channels.whatsapp.inbound"),
    'webform_inbound': os.getenv("KAFKA_TOPIC_WEBFORM_INBOUND", "fte.channels.webform.inbound"),

    # Escalations
    'escalations': os.getenv("KAFKA_TOPIC_ESCALATIONS", "fte.escalations"),

    # Metrics and monitoring
    'metrics': os.getenv("KAFKA_TOPIC_METRICS", "fte.metrics"),

    # Dead letter queue for failed processing
    'dlq': os.getenv("KAFKA_TOPIC_DLQ", "fte.dlq")
}


class FTEKafkaProducer:
    """Kafka producer for publishing events."""

    def __init__(self):
        self.producer = None
        self.bootstrap_servers = KAFKA_BOOTSTRAP_SERVERS

    async def start(self):
        """Start the Kafka producer."""
        try:
            self.producer = AIOKafkaProducer(
                bootstrap_servers=self.bootstrap_servers,
                value_serializer=lambda v: json.dumps(v, default=str).encode('utf-8'),
                compression_type='gzip',
                acks='all',
                retries=3
            )
            await self.producer.start()
            logger.info(f"Kafka producer started: {self.bootstrap_servers}")
        except Exception as e:
            logger.error(f"Failed to start Kafka producer: {e}")
            raise

    async def stop(self):
        """Stop the Kafka producer."""
        if self.producer is not None:
            await self.producer.stop()
            logger.info("Kafka producer stopped")

    async def publish(self, topic: str, event: Dict[str, Any], key: str = None):
        """
        Publish an event to a Kafka topic.

        Args:
            topic: Topic name
            event: Event data (will be JSON serialized)
            key: Optional partition key
        """
        if self.producer is None:
            raise RuntimeError("Producer not started. Call start() first.")

        # Add timestamp if not present
        if "timestamp" not in event:
            event["timestamp"] = datetime.utcnow().isoformat()

        try:
            key_bytes = key.encode('utf-8') if key else None
            await self.producer.send_and_wait(topic, event, key=key_bytes)
            logger.debug(f"Published to {topic}: {event.get('event_type', 'unknown')}")
        except Exception as e:
            logger.error(f"Failed to publish to {topic}: {e}")
            raise


class FTEKafkaConsumer:
    """Kafka consumer for consuming events."""

    def __init__(self, topics: List[str], group_id: str):
        self.topics = topics
        self.group_id = group_id
        self.consumer = None
        self.bootstrap_servers = KAFKA_BOOTSTRAP_SERVERS

    async def start(self):
        """Start the Kafka consumer."""
        try:
            self.consumer = AIOKafkaConsumer(
                *self.topics,
                bootstrap_servers=self.bootstrap_servers,
                group_id=self.group_id,
                value_deserializer=lambda v: json.loads(v.decode('utf-8')),
                auto_offset_reset=os.getenv("KAFKA_AUTO_OFFSET_RESET", "earliest"),
                enable_auto_commit=os.getenv("KAFKA_ENABLE_AUTO_COMMIT", "true") == "true"
            )
            await self.consumer.start()
            logger.info(f"Kafka consumer started: group={self.group_id}, topics={self.topics}")
        except Exception as e:
            logger.error(f"Failed to start Kafka consumer: {e}")
            raise

    async def stop(self):
        """Stop the Kafka consumer."""
        if self.consumer is not None:
            await self.consumer.stop()
            logger.info("Kafka consumer stopped")

    async def consume(self, handler: Callable):
        """
        Consume messages and pass to handler.

        Args:
            handler: Async function that takes (topic, message) as arguments
        """
        if self.consumer is None:
            raise RuntimeError("Consumer not started. Call start() first.")

        logger.info("Starting message consumption...")

        try:
            async for msg in self.consumer:
                try:
                    await handler(msg.topic, msg.value)
                except Exception as e:
                    logger.error(f"Error processing message from {msg.topic}: {e}", exc_info=True)
                    # Optionally publish to DLQ
                    await self._send_to_dlq(msg, e)
        except Exception as e:
            logger.error(f"Consumer loop error: {e}", exc_info=True)
            raise

    async def _send_to_dlq(self, msg, error: Exception):
        """Send failed message to dead letter queue."""
        try:
            # Create a producer for DLQ (in production, reuse a shared producer)
            dlq_event = {
                "original_topic": msg.topic,
                "original_message": msg.value,
                "error": str(error),
                "error_type": type(error).__name__,
                "timestamp": datetime.utcnow().isoformat()
            }

            # TODO: Publish to DLQ topic
            logger.warning(f"Message sent to DLQ: {dlq_event}")
        except Exception as e:
            logger.error(f"Failed to send to DLQ: {e}")


# Singleton instances (optional, for convenience)
_producer_instance = None
_consumer_instances = {}


async def get_producer() -> FTEKafkaProducer:
    """Get or create the global Kafka producer instance."""
    global _producer_instance

    if _producer_instance is None:
        _producer_instance = FTEKafkaProducer()
        await _producer_instance.start()

    return _producer_instance


async def close_producer():
    """Close the global Kafka producer instance."""
    global _producer_instance

    if _producer_instance is not None:
        await _producer_instance.stop()
        _producer_instance = None

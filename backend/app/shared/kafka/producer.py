from __future__ import annotations

import asyncio
import json
import logging
from typing import Any

from aiokafka import AIOKafkaProducer

from app.config import get_settings

logger = logging.getLogger(__name__)


class KafkaEventProducer:
    def __init__(self, producer: AIOKafkaProducer, topic: str) -> None:
        self._producer = producer
        self._topic = topic

    async def publish(self, event_type: str, payload: dict[str, Any]) -> None:
        message = {
            "event_type": event_type,
            "payload": payload,
        }
        body = json.dumps(message, ensure_ascii=False, default=str).encode("utf-8")
        await self._producer.send_and_wait(self._topic, body)
        logger.info("Published kafka event %s to %s", event_type, self._topic)

    async def stop(self) -> None:
        await self._producer.stop()


_producer: KafkaEventProducer | None = None


async def init_kafka_producer(retries: int = 30, delay_seconds: float = 2.0) -> KafkaEventProducer:
    global _producer
    settings = get_settings()
    last_error: Exception | None = None

    for attempt in range(1, retries + 1):
        raw = AIOKafkaProducer(bootstrap_servers=settings.kafka_bootstrap_servers)
        try:
            await raw.start()
            _producer = KafkaEventProducer(raw, settings.kafka_checks_topic)
            logger.info("Kafka producer connected on attempt %s", attempt)
            return _producer
        except Exception as exc:
            last_error = exc
            logger.warning("Kafka producer not ready (attempt %s/%s): %s", attempt, retries, exc)
            try:
                await raw.stop()
            except Exception:
                pass
            await asyncio.sleep(delay_seconds)

    raise RuntimeError(f"Failed to connect Kafka producer: {last_error}")


def get_kafka_producer() -> KafkaEventProducer:
    if _producer is None:
        raise RuntimeError("Kafka producer is not initialized")
    return _producer


async def close_kafka_producer() -> None:
    global _producer
    if _producer is not None:
        await _producer.stop()
    _producer = None

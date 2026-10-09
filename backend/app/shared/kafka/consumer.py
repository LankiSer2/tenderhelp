from __future__ import annotations

import asyncio
import json
import logging

from aiokafka import AIOKafkaConsumer

from app.config import get_settings

logger = logging.getLogger(__name__)


async def run_checks_consumer() -> None:
    settings = get_settings()
    consumer: AIOKafkaConsumer | None = None
    last_error: Exception | None = None

    for attempt in range(1, 31):
        consumer = AIOKafkaConsumer(
            settings.kafka_checks_topic,
            bootstrap_servers=settings.kafka_bootstrap_servers,
            group_id=settings.kafka_consumer_group,
            enable_auto_commit=True,
            auto_offset_reset="earliest",
        )
        try:
            await consumer.start()
            logger.info("Kafka consumer started on topic %s (attempt %s)", settings.kafka_checks_topic, attempt)
            break
        except Exception as exc:
            last_error = exc
            logger.warning("Kafka consumer not ready (attempt %s/30): %s", attempt, exc)
            try:
                await consumer.stop()
            except Exception:
                pass
            consumer = None
            await asyncio.sleep(2)

    if consumer is None:
        raise RuntimeError(f"Failed to start Kafka consumer: {last_error}")

    try:
        async for message in consumer:
            try:
                payload = json.loads(message.value.decode("utf-8"))
                logger.info(
                    "Consumed event=%s check_id=%s identifier=%s is_sme=%s",
                    payload.get("event_type"),
                    payload.get("payload", {}).get("id"),
                    payload.get("payload", {}).get("identifier"),
                    payload.get("payload", {}).get("is_sme"),
                )
            except Exception:
                logger.exception("Failed to process kafka message")
    finally:
        await consumer.stop()


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
    asyncio.run(run_checks_consumer())


if __name__ == "__main__":
    main()

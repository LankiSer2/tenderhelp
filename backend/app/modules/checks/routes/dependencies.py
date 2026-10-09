from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.checks.repositories import ChecksRepository
from app.modules.checks.services import ChecksService
from app.shared.db.session import get_db_session
from app.shared.kafka.producer import get_kafka_producer
from app.shared.redis.client import get_redis_cache


def get_checks_service(session: AsyncSession = Depends(get_db_session)) -> ChecksService:
    return ChecksService(
        repository=ChecksRepository(session),
        cache=get_redis_cache(),
        producer=get_kafka_producer(),
    )

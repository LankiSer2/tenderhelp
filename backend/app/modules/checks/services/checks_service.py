from __future__ import annotations

import logging
from typing import Any

from app.config import get_settings
from app.modules.checks.dto.responses import CheckResponse
from app.modules.checks.events import CheckCompletedEvent
from app.modules.checks.models import SmeCheck
from app.modules.checks.providers import RmspProvider
from app.modules.checks.repositories import ChecksRepository
from app.shared.kafka.producer import KafkaEventProducer
from app.shared.redis.client import RedisCache
from app.shared.validators.identifier import detect_identifier_type

logger = logging.getLogger(__name__)


class ChecksService:
    def __init__(
        self,
        repository: ChecksRepository,
        cache: RedisCache,
        producer: KafkaEventProducer,
        rmsp_provider: RmspProvider | None = None,
    ) -> None:
        self._repository = repository
        self._cache = cache
        self._producer = producer
        self._rmsp = rmsp_provider or RmspProvider()
        self._settings = get_settings()

    def _cache_key(self, identifier: str) -> str:
        return f"sme:check:{identifier}"

    def _to_response(self, entity: SmeCheck, *, from_cache: bool | None = None) -> CheckResponse:
        return CheckResponse(
            id=entity.id,
            identifier=entity.identifier,
            identifier_type=entity.identifier_type,
            is_sme=entity.is_sme,
            sme_category=entity.sme_category,
            company_name=entity.company_name,
            inn=entity.inn,
            ogrn=entity.ogrn,
            from_cache=entity.from_cache if from_cache is None else from_cache,
            created_at=entity.created_at,
        )

    def _response_from_cache(self, cached: dict[str, Any]) -> CheckResponse:
        return CheckResponse.model_validate({**cached, "from_cache": True})

    async def create_check(self, query: str) -> CheckResponse:
        identifier = query
        identifier_type = detect_identifier_type(identifier).value
        cache_key = self._cache_key(identifier)

        cached = await self._cache.get_json(cache_key)
        if cached is not None:
            logger.info("Cache hit for %s", identifier)
            return self._response_from_cache(cached)

        recent = await self._repository.find_recent(identifier, self._settings.cache_ttl_seconds)
        if recent is not None:
            response = self._to_response(recent, from_cache=True)
            await self._cache.set_json(cache_key, response.model_dump(mode="json"))
            return response

        rmsp_result = await self._rmsp.check(identifier)
        entity = SmeCheck(
            identifier=identifier,
            identifier_type=identifier_type,
            is_sme=rmsp_result.is_sme,
            sme_category=rmsp_result.sme_category,
            company_name=rmsp_result.company_name,
            inn=rmsp_result.inn,
            ogrn=rmsp_result.ogrn,
            source_payload=rmsp_result.raw,
            from_cache=False,
        )
        saved = await self._repository.create(entity)
        response = self._to_response(saved, from_cache=False)

        await self._cache.set_json(cache_key, response.model_dump(mode="json"))

        event = CheckCompletedEvent(
            id=saved.id,
            identifier=saved.identifier,
            identifier_type=saved.identifier_type,
            is_sme=saved.is_sme,
            sme_category=saved.sme_category,
            company_name=saved.company_name,
            inn=saved.inn,
            ogrn=saved.ogrn,
            from_cache=False,
            created_at=saved.created_at,
            source_payload=saved.source_payload,
        )
        try:
            await self._producer.publish("sme.check.completed", event.model_dump(mode="json"))
        except Exception:
            logger.exception("Failed to publish kafka event for check %s", saved.id)

        return response

    async def list_checks(self, limit: int = 50, offset: int = 0) -> tuple[list[CheckResponse], int]:
        rows, total = await self._repository.list_checks(limit=limit, offset=offset)
        return [self._to_response(row) for row in rows], total

    async def aclose(self) -> None:
        await self._rmsp.aclose()

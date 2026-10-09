from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import httpx

from app.config import get_settings

CATEGORY_MAP = {
    1: "микропредприятие",
    2: "малое предприятие",
    3: "среднее предприятие",
}


@dataclass(slots=True)
class RmspCheckResult:
    is_sme: bool
    sme_category: str | None
    company_name: str | None
    inn: str | None
    ogrn: str | None
    raw: dict[str, Any] | None


class RmspProvider:
    """Клиент публичного поиска Единого реестра субъектов МСП (rmsp.nalog.ru)."""

    def __init__(self, client: httpx.AsyncClient | None = None) -> None:
        settings = get_settings()
        self._base_url = settings.rmsp_base_url.rstrip("/")
        self._owns_client = client is None
        self._client = client or httpx.AsyncClient(
            timeout=settings.rmsp_timeout_seconds,
            headers={
                "User-Agent": "TenderHelpSMEChecker/1.0",
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "X-Requested-With": "XMLHttpRequest",
            },
        )

    async def check(self, identifier: str) -> RmspCheckResult:
        response = await self._client.post(
            f"{self._base_url}/search-proc.json",
            data={
                "mode": "quick",
                "query": identifier,
                "sortField": "NAME_EX",
                "sort": "ASC",
                "page": "1",
                "pageSize": "10",
            },
        )
        response.raise_for_status()
        payload = response.json()
        rows = payload.get("data") or []
        if not rows:
            return RmspCheckResult(
                is_sme=False,
                sme_category=None,
                company_name=None,
                inn=None,
                ogrn=None,
                raw=payload,
            )

        row = rows[0]
        category_code = row.get("category")
        return RmspCheckResult(
            is_sme=True,
            sme_category=CATEGORY_MAP.get(category_code, str(category_code) if category_code is not None else None),
            company_name=row.get("name_ex") or row.get("name"),
            inn=str(row.get("inn")) if row.get("inn") is not None else None,
            ogrn=str(row.get("ogrn")) if row.get("ogrn") is not None else None,
            raw=payload,
        )

    async def aclose(self) -> None:
        if self._owns_client:
            await self._client.aclose()

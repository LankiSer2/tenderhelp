from __future__ import annotations

from datetime import datetime, timedelta, timezone

from sqlalchemy import Select, desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.checks.models import SmeCheck


class ChecksRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, entity: SmeCheck) -> SmeCheck:
        self._session.add(entity)
        await self._session.commit()
        await self._session.refresh(entity)
        return entity

    async def list_checks(self, limit: int = 50, offset: int = 0) -> tuple[list[SmeCheck], int]:
        total = await self._session.scalar(select(func.count()).select_from(SmeCheck)) or 0
        stmt: Select[tuple[SmeCheck]] = (
            select(SmeCheck).order_by(desc(SmeCheck.created_at)).limit(limit).offset(offset)
        )
        rows = (await self._session.scalars(stmt)).all()
        return list(rows), int(total)

    async def find_recent(self, identifier: str, within_seconds: int) -> SmeCheck | None:
        threshold = datetime.now(timezone.utc) - timedelta(seconds=within_seconds)
        stmt = (
            select(SmeCheck)
            .where(SmeCheck.identifier == identifier, SmeCheck.created_at >= threshold)
            .order_by(desc(SmeCheck.created_at))
            .limit(1)
        )
        return await self._session.scalar(stmt)

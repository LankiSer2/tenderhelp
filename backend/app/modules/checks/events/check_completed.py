from datetime import datetime
from typing import Any

from pydantic import BaseModel


class CheckCompletedEvent(BaseModel):
    id: str
    identifier: str
    identifier_type: str
    is_sme: bool
    sme_category: str | None = None
    company_name: str | None = None
    inn: str | None = None
    ogrn: str | None = None
    from_cache: bool
    created_at: datetime
    source_payload: dict[str, Any] | None = None

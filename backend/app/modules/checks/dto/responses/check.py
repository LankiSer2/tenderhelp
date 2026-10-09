from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CheckResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    identifier: str
    identifier_type: str
    is_sme: bool
    sme_category: str | None = None
    company_name: str | None = None
    inn: str | None = None
    ogrn: str | None = None
    from_cache: bool = False
    created_at: datetime


class CheckListResponse(BaseModel):
    items: list[CheckResponse]
    total: int

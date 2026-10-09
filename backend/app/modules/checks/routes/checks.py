from fastapi import APIRouter, Depends, Query

from app.modules.checks.dto.requests import CreateCheckRequest
from app.modules.checks.dto.responses import CheckListResponse, CheckResponse
from app.modules.checks.routes.dependencies import get_checks_service
from app.modules.checks.services import ChecksService

router = APIRouter(prefix="/api/checks", tags=["checks"])


@router.post("", response_model=CheckResponse, status_code=201)
async def create_check(
    body: CreateCheckRequest,
    service: ChecksService = Depends(get_checks_service),
) -> CheckResponse:
    return await service.create_check(body.query)


@router.get("", response_model=CheckListResponse)
async def list_checks(
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    service: ChecksService = Depends(get_checks_service),
) -> CheckListResponse:
    items, total = await service.list_checks(limit=limit, offset=offset)
    return CheckListResponse(items=items, total=total)

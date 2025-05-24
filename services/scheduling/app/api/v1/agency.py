from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends
from app.api.v1.dependencies import require_role
from app.crud.crud_agency import create_agency, get_agency_by_name
from app.db.deps import get_db
from app.schemas.agency import AgencyCreate, AgencyOut
from app.schemas.error import ErrorResponse
from app.models.agency import RoleEnum
import app.core.exceptions as api_exceptions

router = APIRouter(prefix="/agency", tags=["agency"])

@router.post(
    "/register",
    dependencies=[Depends(require_role(RoleEnum.CENTER_ADMIN))],
    response_model=AgencyOut,
    responses={
        400: {"model": ErrorResponse, "description": "Agency already registered"},
        422: {"model": ErrorResponse, "description": "Validation Error"},
    },
)
async def register_agency(agency_in: AgencyCreate, db: AsyncSession = Depends(get_db)):
    if await get_agency_by_name(db, agency_in.name):
        raise api_exceptions.AgencyAlreadyRegistered(agency_in.name)
    return await create_agency(db, agency_in)


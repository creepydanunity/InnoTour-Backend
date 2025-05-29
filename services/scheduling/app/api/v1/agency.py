from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends
from app.api.v1.dependencies import require_internal_api_key, require_role
from app.crud.crud_agency import create_agency, delete_agency, get_agency, update_agency
from app.db.deps import get_db
from app.schemas.agency import AgencyBase, AgencyIn, AgencyOut, AgencyUpdate, UserIn
from app.schemas.error import ErrorResponse
from app.models.agency import RoleEnum

router = APIRouter(prefix="/agency", tags=["agency"])

@router.post(
    "/register",
    dependencies=[Depends(require_role(RoleEnum.CENTER_ADMIN))],
    response_model=AgencyOut,
    responses={
        400: {"model": ErrorResponse, "description": "Agency already registered"},
        403: {"model": ErrorResponse, "description": "Not enough permissions"},
        422: {"model": ErrorResponse, "description": "Validation Error"},
    },
)
async def register_agency(agency_in: AgencyIn, db: AsyncSession = Depends(get_db)):
    return await create_agency(db, agency_in)

@router.post(
    "/update_info",
    dependencies=[Depends(require_role(RoleEnum.CENTER_ADMIN))],
    response_model=AgencyOut,
    responses={
        403: {"model": ErrorResponse, "description": "Not enough permissions"},
        404: {"model": ErrorResponse, "description": "Agency not found"},
        422: {"model": ErrorResponse, "description": "Validation Error"},
    },
)
async def update_agency_info(agency_in: AgencyUpdate, db: AsyncSession = Depends(get_db)):
    return await update_agency(db, agency_in)

@router.delete(
    "/delete",
    dependencies=[Depends(require_role(RoleEnum.CENTER_ADMIN))],
    response_model={"result": bool},
    responses={
        403: {"model": ErrorResponse, "description": "Not enough permissions"},
        404: {"model": ErrorResponse, "description": "Agency not found"},
        422: {"model": ErrorResponse, "description": "Validation Error"},
    },
)
async def delete_agency_info(agency_in: AgencyBase, db: AsyncSession = Depends(get_db)):
    return await delete_agency(db, agency_in.id)

@router.get(
    "/get",
    response_model=AgencyOut,
    dependencies=[Depends(require_internal_api_key)],
    responses={
        403: {"model": ErrorResponse, "description": "Not enough permissions"},
        404: {"model": ErrorResponse, "description": "Agency not found"},
        422: {"model": ErrorResponse, "description": "Validation Error"},
    },
)
async def get_agency_info(user_in: UserIn, db: AsyncSession = Depends(get_db)):
    return await get_agency(db, user_in.id)

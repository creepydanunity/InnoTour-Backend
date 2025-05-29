from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends
from app.api.v1.dependencies import require_internal_api_key, require_role
from app.crud.crud_slot_category import create_category, update_category
from app.db.deps import get_db
from app.schemas.slot_category import CategoryBase, CategoryIn, CategoryUpdate
from app.schemas.error import ErrorResponse
from app.models.agency import RoleEnum

router = APIRouter(prefix="/category", tags=["category"])

@router.post(
    "/create",
    dependencies=[Depends(require_role(RoleEnum.CENTER_ADMIN))],
    response_model=CategoryUpdate,
    responses={
        400: {"model": ErrorResponse, "description": "Category already exists"},
        403: {"model": ErrorResponse, "description": "Not enough permissions"},
        422: {"model": ErrorResponse, "description": "Validation Error"},
    },
)
async def create_new_category(category_in: CategoryIn, db: AsyncSession = Depends(get_db)):
    return await create_category(db, category_in)

@router.post(
    "/update_info",
    dependencies=[Depends(require_role(RoleEnum.CENTER_ADMIN))],
    response_model=CategoryUpdate,
    responses={
        403: {"model": ErrorResponse, "description": "Not enough permissions"},
        404: {"model": ErrorResponse, "description": "Category not found"},
        422: {"model": ErrorResponse, "description": "Validation Error"},
    },
)
async def update_category_info(data: CategoryUpdate, db: AsyncSession = Depends(get_db)):
    return await update_category(db, data)
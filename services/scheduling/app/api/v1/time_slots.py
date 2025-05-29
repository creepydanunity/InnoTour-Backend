from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends
from app.api.v1.dependencies import require_role
from app.db.deps import get_db
from app.schemas.error import ErrorResponse
from app.models.agency import RoleEnum
from app.schemas.slot import SlotCapacity, SlotIn, TimeSlotsInfo
from app.crud.crud_timeslot import get_timeslots

router = APIRouter(prefix="/time_slot", tags=["time_slot"])

@router.post(
    "/get_info",
    dependencies=[Depends(require_role(RoleEnum.AGENCY_MANAGER))],
    response_model=TimeSlotsInfo,
    responses={
        403: {"model": ErrorResponse, "description": "Not enough permissions"},
        422: {"model": ErrorResponse, "description": "Validation Error"},
    },
)
async def get_slots_info(data: SlotIn, db: AsyncSession = Depends(get_db)):
    capacity_by_slot = await get_timeslots(db, data.day)
    slots = [
        SlotCapacity(
            id=slot.id,
            slot_time=slot.slot_time,
            capacity=capacity,
        )
        for slot, capacity in capacity_by_slot.items()
    ]
    return TimeSlotsInfo(slots=slots)
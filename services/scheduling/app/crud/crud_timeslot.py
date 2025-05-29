from datetime import date, timedelta, datetime, time
from typing import Dict, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.time_slot import TimeSlot
from app.core.exceptions import TimeSlotsMissing


async def get_timeslots(db: AsyncSession, data: date) -> Dict[TimeSlot, int]:
    stmt = (
        select(TimeSlot)
        .where(TimeSlot.slot_date == data.day)
        .options(selectinload(TimeSlot.bookings))
        .options(selectinload(TimeSlot.category))
        .order_by(TimeSlot.slot_time)
    )
    result = await db.execute(stmt)
    timeslots: List[TimeSlot] = list(result.scalars().all())

    capacity_by_slot: Dict[TimeSlot, int] = {
        slot: slot.category.capacity - sum([booking.participants_count for booking in slot.bookings])
        for slot in timeslots
    }

    if not capacity_by_slot:
        raise TimeSlotsMissing()
    
    return capacity_by_slot

async def create_initial_timeslots(db: AsyncSession) -> str:
    start_date = date.today()

    end_date = start_date + timedelta(days=182)

    slots = []
    for day_offset in range((end_date - start_date).days):
        current_date = start_date + timedelta(days=day_offset)

        category_id = 1 if current_date.weekday() < 5 else 2

        slot_dt = datetime.combine(current_date, time(7, 30))
        last_dt = datetime.combine(current_date, time(18, 00))
        while slot_dt <= last_dt:
            slots.append(
                TimeSlot(
                    slot_date=current_date,
                    slot_time=slot_dt.time(),
                    category_id=category_id,
                )
            )
            slot_dt += timedelta(minutes=30)

    db.add_all(slots)
    await db.commit()

    return f"Created {len(slots)} slots" \
           f"Start date: {start_date}, end date: {end_date}"

async def create_daily_timeslot(db: AsyncSession) -> str:
    slots_date = date.today()

    slots = []

    category_id = 1 if slots_date.weekday() < 5 else 2

    slot_dt = datetime.combine(slots_date, time(7, 30))
    last_dt = datetime.combine(slots_date, time(18, 00))
    while slot_dt <= last_dt:
        slots.append(
            TimeSlot(
                slot_date=slots_date,
                slot_time=slot_dt.time(),
                category_id=category_id,
            )
        )
        slot_dt += timedelta(minutes=30)
    
    db.add_all(slots)
    await db.commit()

    return f"Created {len(slots)} slots" \
           f"Date: {slots_date}"
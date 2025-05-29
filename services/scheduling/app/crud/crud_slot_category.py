from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.slot_category import SlotCategory
from app.schemas.slot_category import CategoryIn, CategoryUpdate
from app.core.exceptions import CategoryAlreadyCreated, CategoryNotFound

async def create_category(db: AsyncSession, data: CategoryIn) -> SlotCategory:
    stmt = (
        select(SlotCategory)
        .where(SlotCategory.name == data.name)
    )
    result = await db.execute(stmt)

    if result.scalars().first():
        raise CategoryAlreadyCreated(data.name)
    
    slotCategory = SlotCategory(
        name=data.name,
        capacity=data.capacity
    )
    db.add(slotCategory)
    await db.commit()
    await db.refresh(slotCategory)

    return slotCategory

async def update_category(db: AsyncSession, data: CategoryUpdate) -> SlotCategory:
    slotCategory = await db.get(SlotCategory, data.id)
    if not slotCategory:
        raise CategoryNotFound()
    
    slotCategory.name = data.name
    slotCategory.capacity = data.capacity

    db.add(slotCategory)
    await db.commit()
    await db.refresh(slotCategory)

    return slotCategory
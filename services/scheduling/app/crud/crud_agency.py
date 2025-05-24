from sqlalchemy import select
from app.core.exceptions import AgencyNotFound
from app.models.agency import Agency
from app.schemas.agency import AgencyCreate, AgencyUpdate
from sqlalchemy.ext.asyncio import AsyncSession

async def create_agency(db: AsyncSession, agency_data: AgencyCreate) -> Agency:
    agency = Agency(
        name=agency_data.name,
        agency_type=agency_data.agency_type
    )

    db.add(agency)
    await db.commit()
    await db.refresh(agency)

    return agency

async def update_agency(db: AsyncSession, new_agency_data: AgencyUpdate) -> Agency:
    agency = await db.get(Agency, new_agency_data.id)
    if not agency:
        raise AgencyNotFound()
    
    agency.name = new_agency_data.name
    agency.agency_type = new_agency_data.agency_type
    
    db.add(agency)
    await db.commit()
    await db.refresh(agency)

    return agency

async def delete_agency(db: AsyncSession, id: int) -> None:
    agency = await db.get(Agency, id)
    if not agency:
        raise AgencyNotFound()
    
    await db.delete(agency)
    await db.commit()

async def get_agency_by_name(db: AsyncSession, name: str) -> Agency | None:
    stmt = (
        select(Agency)
        .where(Agency.name == name)
    )
    result = await db.execute(stmt)
    return result.scalars().first()
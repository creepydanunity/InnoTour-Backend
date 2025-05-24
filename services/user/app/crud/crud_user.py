from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.services.security import hash_password
from app.core.exceptions import UserNotFound

async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    stmt = (
        select(User)
        .where(User.email == email)
    )
    result = await db.execute(stmt)
    return result.scalars().first()

async def create_user(db: AsyncSession, user_in: UserCreate) -> User:
    user = User(
        agency_id=user_in.agency_id,
        email=user_in.email,
        hashed_password=hash_password(user_in.password)
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

async def update_user(db: AsyncSession, new_user_in: UserUpdate) -> User:
    user = await db.get(User, new_user_in.id)
    if not user:
        raise UserNotFound()
    
    user.email = new_user_in.email
    user.role = new_user_in.role
    user.agency_id = new_user_in.agency_id
    
    db.add(user)
    await db.commit()
    await db.refresh(user)

    return user
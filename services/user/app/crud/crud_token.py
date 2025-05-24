from datetime import datetime, timezone
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.token import RefreshToken

async def create_refresh_token_entry(
    db: AsyncSession,
    raw_token: str,
    user_id, expires_at: datetime
) -> RefreshToken:
    token_hash = RefreshToken.hash_token(raw_token)

    db_obj = RefreshToken(user_id=user_id, token_hash=token_hash, expires_at=expires_at)
    db.add(db_obj)

    await db.commit()
    await db.refresh(db_obj)
    return db_obj

async def get_valid_refresh_token(
    db: AsyncSession,
    raw_token: str
) -> RefreshToken | None:
    token_hash = RefreshToken.hash_token(raw_token)

    q = select(RefreshToken).where(
        RefreshToken.token_hash == token_hash,
        RefreshToken.expires_at > datetime.now(timezone.utc),
    )

    result = await db.execute(q)
    return result.scalars().first()

async def consume_refresh_token(db: AsyncSession, raw_token: str) -> bool:
    token_hash = RefreshToken.hash_token(raw_token)
    stmt = (
        delete(RefreshToken)
        .where(
            RefreshToken.token_hash == token_hash,
            RefreshToken.expires_at > datetime.now(timezone.utc),
        )
        .execution_options(synchronize_session="fetch")
    )
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount == 1

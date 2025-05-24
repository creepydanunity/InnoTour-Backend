from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.services.security import decode_token
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.deps import get_db
from app.models.user import RoleEnum, User
from app.crud.crud_user import get_user_by_email
from app.core.exceptions import PermissionRequired, TokenInvalid, UserNotFound

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    try:
        payload = decode_token(token)
    except Exception:
        raise TokenInvalid()
    
    user = await get_user_by_email(db, payload["email"])
    if not user:
        raise UserNotFound()
    
    return user

def require_role(role: RoleEnum):
    def role_checker(user: User = Depends(get_current_user)):
        if user.role != role:
            raise PermissionRequired()
        return user
    return role_checker

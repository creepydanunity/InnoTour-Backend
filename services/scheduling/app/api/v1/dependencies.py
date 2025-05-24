from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt import PyJWTError, decode as jwt_decode
from app.core.config import settings
from app.schemas.token import TokenPayload
from app.core.exceptions import PermissionRequired
from app.models.agency import RoleEnum

bearer_scheme = HTTPBearer()

def get_token_payload(
    creds = Depends(bearer_scheme),
) -> TokenPayload:
    try:
        raw = jwt_decode(
            creds.credentials,
            settings.jwt_key,
            algorithms=[settings.algorithm],
            options={"require": ["exp", "scope"]},
        )
        payload = TokenPayload(**raw)
    except PyJWTError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid token")
    if payload.scope != "access_token":
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Wrong token scope")
    return payload

def require_role(role: RoleEnum):
    def role_checker(payload: TokenPayload = Depends(get_token_payload)):
        if payload.role != role:
            raise PermissionRequired()
        return payload
    return role_checker
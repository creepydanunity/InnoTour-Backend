from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, HTTPException, status
from jwt import PyJWTError

from app.services.security import decode_token

class AuthMiddleware(BaseHTTPMiddleware):
    """
    Middleware that looks for a Bearer token,
    decodes it, and places the payload on request.state.user_payload.
    If decoding fails, it aborts with 401.
    """

    async def dispatch(self, request: Request, call_next):
        auth: str | None = request.headers.get("Authorization")
        if auth and auth.startswith("Bearer "):
            token = auth.split(" ", 1)[1]
            try:
                payload = decode_token(token)
            except PyJWTError:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid or expired token",
                )

            request.state.user_payload = payload
        return await call_next(request)

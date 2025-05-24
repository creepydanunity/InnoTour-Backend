from typing import Optional
from pydantic import BaseModel

class TokenPayload(BaseModel):
    sub: int
    agency_id: Optional[int]
    email: str
    role: str
    exp: int
    iat: int
    scope: str

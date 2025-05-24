from pydantic import BaseModel

from app.schemas.user import UserOut

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenUser(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut
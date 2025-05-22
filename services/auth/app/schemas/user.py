from pydantic import BaseModel, EmailStr
from app.models.user import RoleEnum

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: RoleEnum

    class Config:
        orm_mode = True
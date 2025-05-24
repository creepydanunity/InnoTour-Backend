from typing import Optional
from pydantic import BaseModel, EmailStr
from app.models.user import RoleEnum

class UserCreate(BaseModel):
    agency_id: int
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: RoleEnum
    agency_id: Optional[int] = None

    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    id: int
    agency_id: int
    email: EmailStr
    role: RoleEnum
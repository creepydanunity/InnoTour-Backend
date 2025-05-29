from pydantic import BaseModel
from app.models.agency import AgencyTypeEnum

class AgencyIn(BaseModel):
    name: str
    agency_type: AgencyTypeEnum

class AgencyBase(BaseModel):
    id: int

class AgencyOut(AgencyBase):
    name: str
    agency_type: AgencyTypeEnum
    class Config:
        orm_mode = True

class AgencyUpdate(AgencyBase):
    name: str
    agency_type: AgencyTypeEnum

class UserIn(BaseModel):
    id: int
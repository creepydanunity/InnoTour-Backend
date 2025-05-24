from pydantic import BaseModel
from app.models.agency import AgencyTypeEnum

class AgencyCreate(BaseModel):
    name: str
    agency_type: AgencyTypeEnum

class AgencyOut(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class AgencyUpdate(BaseModel):
    id: int
    name: str
    agency_type: AgencyTypeEnum
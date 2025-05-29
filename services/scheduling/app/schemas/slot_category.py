from pydantic import BaseModel

class CategoryIn(BaseModel):
    name: str
    capacity: int

class CategoryBase(BaseModel):
    id: int

class CategoryUpdate(CategoryBase):
    name: str
    capacity: int
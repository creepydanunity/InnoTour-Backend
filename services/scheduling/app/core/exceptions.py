from typing import Any, Dict
from typing_extensions import Annotated, Doc
from fastapi import HTTPException, status


class AgencyNotFound(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agency not found"
        )

class PermissionRequired(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )

class AgencyAlreadyRegistered(HTTPException):
    def __init__(self, name: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Agency {name} is already registered"
        )

class CategoryAlreadyCreated(HTTPException):
    def __init__(self, name: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Category {name} is already created"
        )

class CategoryNotFound(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )

class TimeSlotsMissing(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Slots not found"
        )
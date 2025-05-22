import enum
from sqlalchemy import Enum
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class RoleEnum(str, enum.Enum):
    CENTER_ADMIN   = "admin"
    AGENCY_MANAGER = "agency_manager"

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[RoleEnum] = mapped_column(Enum(RoleEnum), default=RoleEnum.AGENCY_MANAGER, nullable=False)   
    
    def __repr__(self) -> str:
        return f"<User id={self.id!r} email={self.email!r} role={self.role!r}>"

import enum
from sqlalchemy import Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class AgencyTypeEnum(str, enum.Enum):
    INNER = "innopolis"
    OUTER = "outer"

class Agency(Base):
    __tablename__ = "agencies"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(nullable=False)
    agency_type: Mapped[AgencyTypeEnum] = mapped_column(Enum(AgencyTypeEnum), default=AgencyTypeEnum.INNER, nullable=False)

    def __repr__(self) -> str:
        return f"<Agency id={self.id!r} name={self.name!r}>"

class RoleEnum(str, enum.Enum):
    CENTER_ADMIN   = "admin"
    AGENCY_MANAGER = "agency_manager"
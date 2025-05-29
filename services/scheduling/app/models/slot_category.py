from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from app.models.time_slot import TimeSlot

class SlotCategory(Base):
    __tablename__ = "slot_categories"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(nullable=False)
    capacity: Mapped[int] = mapped_column(nullable=False)

    time_slots: Mapped[list["TimeSlot"]] = relationship(
        "TimeSlot",
        back_populates="category",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self) -> str:
        return f"<Slot Category id={self.id!r} name={self.name!r} capacity={self.capacity!r}>"
import datetime
from typing import List
from sqlalchemy import Date, Time, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class TimeSlot(Base):
    from app.models.slot_category import SlotCategory
    from app.models.booking import Booking

    __tablename__ = "time_slots"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    slot_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    slot_time: Mapped[datetime.time] = mapped_column(Time, nullable=False)

    category_id: Mapped[int] = mapped_column(
        ForeignKey("slot_categories.id"),
        nullable=False
    )

    category: Mapped["SlotCategory"] = relationship(
        "SlotCategory",
        back_populates="time_slots"
    )
    
    bookings: Mapped[List["Booking"]]= relationship(
        "Booking",
        back_populates="time_slot",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self) -> str:
        return (
            f"<TimeSlot id={self.id!r} "
            f"slot_date={self.slot_date!r} "
            f"slot_time={self.slot_time!r}>"
        )
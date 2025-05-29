import datetime
from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from app.models.time_slot import TimeSlot
from app.models.agency import Agency

class Booking(Base):
    __tablename__ = "bookings"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    agency_id: Mapped[int] = mapped_column(
        ForeignKey("agencies.id"),
        nullable=False
    )
    time_slot_id: Mapped[int] = mapped_column(
        ForeignKey("time_slots.id"),
        nullable=False
    )
    participants_count: Mapped[int] = mapped_column(nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())

    agency: Mapped["Agency"] = relationship(
        "Agency",
        back_populates="bookings"
    )

    time_slot: Mapped["TimeSlot"] = relationship(
        "TimeSlot",
        back_populates="bookings"
    )
    
    def __repr__(self) -> str:
        return (
            f"<Booking id={self.id!r} "
            f"agency_id={self.agency_id!r} "
            f"time_slot={self.time_slot_id!r} "
            f"participants_count={self.participants_count!r} "
            f"created_at={self.created_at!r}"
        )
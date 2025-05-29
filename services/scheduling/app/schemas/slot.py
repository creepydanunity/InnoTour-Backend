from typing import List
from pydantic import BaseModel
from datetime import date, time

class SlotIn(BaseModel):
    day: date

class TimeSlot(BaseModel):
    id: int
    slot_time: time

class SlotCapacity(BaseModel):
    id: int
    slot_time: time
    capacity: int

class TimeSlotsInfo(BaseModel):
    slots: List[SlotCapacity]
from datetime import date, datetime
from pydantic import BaseModel
from src.habits.enums import HabitType


class HabitBase(BaseModel):
    name: str
    habit_type: HabitType
    achieved: bool
    archived: bool
    start_at: date


class Habit(HabitBase):
    id: int
    created_at: datetime
    last_update_at: datetime

    class Config:
        orm_mode = True

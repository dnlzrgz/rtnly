from dataclasses import field
from datetime import date, datetime, timezone
from enum import Enum
from sqlmodel import Field, SQLModel


class HabitType(str, Enum):
    BINARY = "binary"
    QUANTITATIVE = "quantitative"


class HabitBase(SQLModel):
    name: str = Field(min_length=1, max_length=255)
    habit_type: HabitType = Field(default=HabitType.BINARY)
    achieved: bool = False
    archived: bool = False
    start_at: date = Field(default=datetime.now(timezone.utc))


class HabitCreate(HabitBase):
    name: str = Field(min_length=1, max_length=255)
    habit_type: HabitType = Field(default=HabitType.BINARY)
    start_at: date = Field(default=datetime.now(timezone.utc))


class HabitUpdate(HabitBase):
    name: str | None = Field(default=None, min_length=1, max_length=255)  # type: ignore
    habit_type: HabitType | None = Field(default=None)  # type: ignore
    achieved: bool | None = field(default=None)  # type: ignore
    archived: bool | None = field(default=None)  # type: ignore
    start_at: date | None = Field(default=None)  # type: ignore


class Habit(HabitBase, table=True):
    __tablename__ = "habits"  # type: ignore

    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default=datetime.now(timezone.utc))
    last_updated_at: datetime = Field(default=datetime.now(timezone.utc))


class HabitPublic(HabitBase):
    id: int


class HabitsPublic(SQLModel):
    data: list[HabitPublic]
    count: int

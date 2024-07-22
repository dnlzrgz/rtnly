from datetime import datetime, timezone
from sqlalchemy import Date, DateTime, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.declarative import declarative_base
from src.habits.enums import HabitType

Base = declarative_base()


class Habit(Base):
    __tablename__ = "habits"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    habit_type: Mapped[HabitType] = mapped_column(
        default=HabitType.BINARY,
    )
    achieved: Mapped[bool] = mapped_column(Boolean(), default=False)
    archived: Mapped[bool] = mapped_column(Boolean(), default=False)
    start_at: Mapped[datetime] = mapped_column(
        Date,
        default=datetime.now(timezone.utc),
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now(timezone.utc),
    )
    last_update_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now(timezone.utc),
    )

    def __repr__(self) -> str:
        # TODO:
        return f"Habit(id={self.id!r}, name={self.name!r})"

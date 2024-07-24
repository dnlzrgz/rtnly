from sqlalchemy import create_engine
from app.config import settings

engine = create_engine(str(settings.SQLITE_URL))


def init_db() -> None:
    # TODO: use Alembic
    from app.models.habits import Habit  # noqa: F401
    from sqlmodel import SQLModel

    SQLModel.metadata.create_all(engine)

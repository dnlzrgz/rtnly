from sqlalchemy import create_engine
from sqlmodel import Session, SQLModel, select
from app.models import HabitCreate, User, UserCreate, Habit  # noqa: F401
from app.config import settings
from app.security import get_password_hash

engine = create_engine(str(settings.SQLITE_URL))


def init_db(session: Session) -> None:
    # TODO: use Alembic
    SQLModel.metadata.create_all(engine)

    user = session.exec(
        select(User).where(User.email == settings.FIRST_ADMIN)
    ).one_or_none()
    if not user:
        user_in = UserCreate(
            email=settings.FIRST_ADMIN,
            password=settings.FIRST_ADMIN_PASSWORD,
            is_admin=True,
        )

        user_db = User.model_validate(
            user_in,
            update={
                "hashed_password": get_password_hash(user_in.password),
            },
        )

        session.add(user_db)
        session.commit()

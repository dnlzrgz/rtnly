import uuid
from enum import Enum
from dataclasses import field
from datetime import date, datetime, timezone
from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel


class HabitType(str, Enum):
    BINARY = "binary"
    QUANTITATIVE = "quantitative"


class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_admin: bool = False


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)


class UserRegister(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    password: str = Field(min_length=8, max_length=40)


class UserUpdate(UserBase):
    email: EmailStr | None = Field(default=None, max_length=255)  # type: ignore
    password: str | None = Field(default=None, min_length=8, max_length=40)


class UserUpdateMe(SQLModel):
    email: EmailStr | None = Field(default=None, max_length=255)  # type: ignore


class UpdatePassword(SQLModel):
    old_password: str = Field(min_length=8, max_length=40)
    new_password: str = Field(min_length=8, max_length=40)


class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str

    habits: list["Habit"] = Relationship(back_populates="owner")


class UserPublic(UserBase):
    id: uuid.UUID


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int


class HabitBase(SQLModel):
    name: str = Field(min_length=1, max_length=255)
    habit_type: HabitType = Field(default=HabitType.BINARY)
    achieved: bool = False
    archived: bool = False
    start_at: date = Field(default=datetime.now(timezone.utc).date())


class HabitCreate(HabitBase):
    name: str = Field(min_length=1, max_length=255)
    habit_type: HabitType = Field(default=HabitType.BINARY)
    start_at: date = Field(default=datetime.now(timezone.utc).date())


class HabitUpdate(HabitBase):
    name: str | None = Field(default=None, min_length=1, max_length=255)  # type: ignore
    habit_type: HabitType | None = Field(default=None)  # type: ignore
    achieved: bool | None = field(default=None)  # type: ignore
    archived: bool | None = field(default=None)  # type: ignore
    start_at: date | None = Field(default=None)  # type: ignore


class Habit(HabitBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default=datetime.now(timezone.utc))
    last_updated_at: datetime = Field(default=datetime.now(timezone.utc))

    owner_id: uuid.UUID = Field(foreign_key="user.id", nullable=False)
    owner: User | None = Relationship(back_populates="habits")


class HabitPublic(HabitBase):
    id: uuid.UUID
    owner_id: uuid.UUID


class HabitsPublic(SQLModel):
    data: list[HabitPublic]
    count: int


class Message(SQLModel):
    message: str


class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(SQLModel):
    sub: str | None = None


class NewPassword(SQLModel):
    token: str
    new_password: str = Field(min_length=8, max_length=40)

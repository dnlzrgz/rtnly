import uuid
from typing import Any
from fastapi import APIRouter, HTTPException, status
from sqlmodel import func, select
from app.models import (
    Habit,
    HabitCreate,
    HabitPublic,
    HabitsPublic,
    HabitUpdate,
    Message,
)
from app.dependencies import CurrentUser, SessionDep

router = APIRouter(
    prefix="/habits",
    tags=["habits"],
)


@router.get("/", response_model=HabitsPublic)
async def read_habits(
    session: SessionDep,
    current_user: CurrentUser,
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve habits.
    """

    count_stmt = (
        select(func.count()).select_from(Habit).where(Habit.owner_id == current_user.id)
    )
    count = session.exec(count_stmt).one()

    stmt = (
        select(Habit).where(Habit.owner_id == current_user.id).offset(skip).limit(limit)
    )
    habits = session.exec(stmt).all()
    return HabitsPublic(data=habits, count=count)


@router.get("/{id}", response_model=HabitPublic)
async def read_habit(
    session: SessionDep,
    current_user: CurrentUser,
    id: uuid.UUID,
) -> Any:
    """
    Get habit by ID.
    """

    habit = session.get(Habit, id)
    if not habit or habit.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Habit not found",
        )

    return habit


@router.post("/", response_model=HabitPublic)
async def create_habit(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    habit_in: HabitCreate,
) -> Any:
    """
    Create new habit.
    """

    habit = Habit.model_validate(
        habit_in,
        update={"owner_id": current_user.id},
    )

    session.add(habit)
    session.commit()
    session.refresh(habit)

    return habit


@router.put("/{id}")
async def update_habit(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    id: uuid.UUID,
    habit_in: HabitUpdate,
) -> Any:
    """
    Update a habit.
    """

    habit = session.get(Habit, id)
    if not habit or habit.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Habit not found",
        )

    update_dict = habit_in.model_dump(exclude_unset=True)
    habit.sqlmodel_update(update_dict)

    session.add(habit)
    session.commit()
    session.refresh(habit)

    return habit


@router.delete("/{id}")
async def delete_habit(
    session: SessionDep,
    current_user: CurrentUser,
    id: uuid.UUID,
) -> Any:
    """
    Delete habit.
    """

    habit = session.get(Habit, id)
    if not habit or habit.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Habit not found",
        )

    session.delete(habit)
    session.commit()

    return Message(message="Habit deleted successfully")

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
    Record,
    RecordCreate,
    RecordPublic,
    RecordsPublic,
    RecordUpdate,
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


@router.get("/{habit_id}/records/", response_model=RecordsPublic)
async def read_records_for_habit(
    session: SessionDep,
    current_user: CurrentUser,
    habit_id: uuid.UUID,
    skip: int = 0,
    limit: int = 100,
):
    """
    Retrieve record for specific habit.
    """

    habit = session.get(Habit, habit_id)
    if not habit or habit.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Habit not found",
        )

    count_stmt = (
        select(func.count()).select_from(Record).where(Record.habit_id == habit_id)
    )
    count = session.exec(count_stmt).one()

    stmt = select(Record).where(Record.habit_id == habit_id).offset(skip).limit(limit)
    records = session.exec(stmt).all()
    return HabitsPublic(data=records, count=count)


@router.post("/{habit_id}/records/", response_model=RecordPublic)
async def create_record_for_habit(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    habit_id: uuid.UUID,
    record_in: RecordCreate,
):
    """
    Create record for specific habit.
    """

    habit = session.get(Habit, habit_id)
    if not habit or habit.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Habit not found",
        )

    record = Record.model_validate(
        record_in,
        update={
            "owner_id": current_user.id,
            "habit_id": habit_id,
        },
    )

    session.add(record)
    session.commit()
    session.refresh(record)

    return record


@router.get("/{habit_id}/records/{record_id}", response_model=RecordPublic)
async def read_record_for_habit(
    session: SessionDep,
    current_user: CurrentUser,
    habit_id: uuid.UUID,
    record_id: uuid.UUID,
):
    """
    Get specific record associated with a habit.
    """

    habit = session.get(Habit, habit_id)
    if not habit or habit.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Habit not found",
        )

    record = session.get(Record, record_id)
    if not record or record.habit_id != habit_id or record.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Record not found",
        )

    return record


@router.put("/{habit_id}/records/{record_id}", response_model=RecordPublic)
async def update_record_for_habit(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    habit_id: uuid.UUID,
    record_id: uuid.UUID,
    record_in: RecordUpdate,
):
    """
    Update specific record.
    """

    habit = session.get(Habit, habit_id)
    if not habit or habit.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Habit not found",
        )

    record = session.get(Record, record_id)
    if not record or record.habit_id != habit_id or record.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Record not found",
        )

    update_dict = record_in.model_dump(exclude_unset=True)
    record.sqlmodel_update(update_dict)

    session.add(record)
    session.commit()
    session.refresh(record)

    return record

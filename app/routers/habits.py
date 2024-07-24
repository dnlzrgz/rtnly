from fastapi import APIRouter

router = APIRouter(
    prefix="/habits",
    tags=["habits"],
)


@router.get("/")
async def read_habits():
    return {"message": "read_habits"}


@router.post("/")
async def create_habit():
    return {"message": "create_habit"}


@router.get("/{habit_id}")
async def read_habit(habit_id: int):
    return {"message": "read_habit"}


@router.put("/{habit_id}")
async def update_habit(habit_id: int):
    return {"message": "update_habit"}


@router.delete("/{habit_id}")
async def delete_habit(habit_id: int):
    return {"message": "delete_habit"}

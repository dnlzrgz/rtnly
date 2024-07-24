from fastapi import FastAPI
from app.routers.habits import router as habits_router
from app.db import init_db

init_db()

app = FastAPI()


app.include_router(habits_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}

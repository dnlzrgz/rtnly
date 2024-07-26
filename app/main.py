from fastapi import FastAPI
from app.config import settings
from app.routers.habits import router as habits_router
from app.routers.auth import router as auth_router
from app.init import init

init()

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)


app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(habits_router, prefix=settings.API_V1_STR)

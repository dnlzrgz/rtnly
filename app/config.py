import secrets
from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
    )

    PROJECT_NAME: str = "rtnly"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    DOMAIN: str = "localhost"
    ENVIROMENT: Literal["development", "staging", "production"] = "development"
    SQLITE_FILE_NAME: str = "db.sqlite3"
    SQLITE_URL: str = f"sqlite:///{SQLITE_FILE_NAME}"

    FIRST_ADMIN: str
    FIRST_ADMIN_PASSWORD: str
    USERS_OPEN_REGISTRATION: bool = False

    @property
    def server_host(self) -> str:
        # TODO: Add http depending on the enviroment
        return f"http://{self.DOMAIN}"


settings = Settings()  # type: ignore

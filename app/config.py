from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
    )

    API_V1_STR: str = "/api/v1"
    DOMAIN: str = "localhost"
    ENVIROMENT: Literal["development", "staging", "production"] = "development"
    SQLITE_FILE_NAME: str = "db.sqlite3"

    @property
    def server_host(self) -> str:
        # TODO: Add http depending on the enviroment
        return f"http://{self.DOMAIN}"

    @property
    def SQLITE_URL(self) -> str:
        return f"sqlite:///{self.SQLITE_FILE_NAME}"


settings = Settings()

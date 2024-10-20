from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_NAME: str

    @computed_field
    @property
    def db_url(self) -> str:
      return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}/{self.DB_NAME}"

settings = Settings()

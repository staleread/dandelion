from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    jwt_secret: str
    jwt_algorithm: str
    jwt_lifetime: int
    db_user: str
    db_pass: str
    db_host: str
    db_name: str

    @computed_field  # type: ignore
    @property
    def db_url(self) -> str:
        return f"postgresql+psycopg://{self.db_user}:{self.db_pass}@{self.db_host}/{self.db_name}"

import bcrypt
from app.core.config import Settings

salt = Settings().hash_salt.encode("utf-8")  # type: ignore


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

import jwt
from datetime import datetime, timezone, timedelta

from app.core.config import Settings
from ...domain.models import UserLoginInfo

settings = Settings()  # type: ignore

key = settings.jwt_secret
algorithm = settings.jwt_algorithm
exp_seconds = settings.jwt_lifetime


def encode_user_login_info(login_info: UserLoginInfo) -> str:
    data = {
        "exp": get_timestamp_after_seconds(exp_seconds),
        **login_info.model_dump(),
    }
    return jwt.encode(data, key, algorithm=algorithm)


def decode_user_login_info(token: str) -> UserLoginInfo | None:
    try:
        payload = jwt.decode(token, key, algorithms=[algorithm])
        return UserLoginInfo(**payload)
    except jwt.ExpiredSignatureError:
        return None


def get_timestamp_after_seconds(seconds: int) -> int:
    moment = datetime.now(tz=timezone.utc) + timedelta(seconds=seconds)
    return int(moment.timestamp())

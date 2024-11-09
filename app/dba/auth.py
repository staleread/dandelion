import jwt
from typing import Annotated
from datetime import datetime, timezone, timedelta
from fastapi import Cookie, Depends

from app.core.config import Settings
from .models import UserLoginInfo, UserInfo
from .enums import Permission


settings = Settings()  # type: ignore

key = settings.jwt_secret
algorithm = settings.jwt_algorithm
exp_seconds = settings.jwt_lifetime


def encode_user_login_info(login_info: UserLoginInfo) -> str:
    data = {
        "exp": get_timestamp_after_seconds(exp_seconds),
        "user_data": login_info.model_dump(),
    }
    return jwt.encode(data, key, algorithm=algorithm)


def decode_user_login_info(token: str) -> UserLoginInfo | None:
    try:
        payload = jwt.decode(token, key, algorithms=[algorithm])
        return UserLoginInfo(**payload["user_data"])
    except jwt.ExpiredSignatureError:
        return None


def get_timestamp_after_seconds(seconds: int) -> int:
    moment = datetime.now(tz=timezone.utc) + timedelta(seconds=seconds)
    return int(moment.timestamp())


def current_user(*permissions: set[Permission]):
    def get_user(id_token: Annotated[str | None, Cookie()] = None) -> UserInfo | None:
        if not id_token:
            return None

        login_info = decode_user_login_info(id_token)

        if not login_info:
            return None

        user_info = UserInfo(username=login_info.username)

        if set(login_info.permissions) >= set(permissions):
            user_info.is_authorized = True

        return user_info

    return get_user


permissions = [
    Permission.CAN_CONNECT,
    Permission.CAN_READ_PUBLIC,
    Permission.CAN_MODIFY_RECORDS,
    Permission.CAN_MODIFY_ATTRIBUTES,
    Permission.CAN_ADD_USER,
    Permission.CAN_ADD_OPERATOR,
    Permission.CAN_READ_PRIVATE,
    Permission.CAN_MODIFY_TABLES,
    Permission.CAN_ADD_ADMIN,
]

Guest = Annotated[UserInfo | None, Depends(current_user(*permissions[:2]))]
Operator = Annotated[UserInfo | None, Depends(current_user(*permissions[:3]))]
Admin = Annotated[UserInfo | None, Depends(current_user(*permissions[:5]))]
Owner = Annotated[UserInfo | None, Depends(current_user(*permissions[:]))]

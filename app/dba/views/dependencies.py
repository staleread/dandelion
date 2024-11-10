from typing import Annotated
from pydantic.dataclasses import dataclass
from fastapi import Cookie, Depends

from .utils.jwt import decode_user_login_info
from ..domain.enums import Permission


@dataclass
class UserInfo:
    username: str
    is_authorized: bool = False


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

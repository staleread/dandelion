from typing import Annotated
from pydantic.dataclasses import dataclass
from fastapi import Cookie, Depends, HTTPException

from .utils.jwt import decode_user_login_info
from ..data.models import Permission


@dataclass
class UserInfo:
    username: str
    permissions: set[Permission]


def current_user(*permissions: set[Permission]):
    def get_user(id_token: Annotated[str | None, Cookie()] = None) -> UserInfo:
        if not id_token:
            raise HTTPException(status_code=401, detail="Unauthorized")

        login_info = decode_user_login_info(id_token)

        if not login_info:
            raise HTTPException(status_code=401, detail="Unauthorized")

        user_info = UserInfo(
            username=login_info.username,
            permissions=set(map(Permission, login_info.permissions)),
        )

        if not set(login_info.permissions) >= set(permissions):
            raise HTTPException(status_code=403, detail="Forbidden")

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


def get_guest_user():
    return current_user(*permissions[:2])


def get_operator_user():
    return current_user(*permissions[:3])


def get_admin_user():
    return current_user(*permissions[:5])


def get_owner_user():
    return current_user(*permissions)


GuestDep = Annotated[UserInfo, Depends(get_guest_user())]
OperatorDep = Annotated[UserInfo, Depends(get_operator_user())]
AdminDep = Annotated[UserInfo, Depends(get_admin_user())]
OwnerDep = Annotated[UserInfo, Depends(get_owner_user())]

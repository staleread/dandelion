from fastapi import HTTPException, Depends, Cookie
from typing import Annotated

from .service import retrieve_user_info
from .enums import Permissions
from .models import UserInfo


def current_user(*permissions: Permissions):
    def get_user(id_token: Annotated[str | None, Cookie()] = None) -> UserInfo:
        if not id_token:
            raise HTTPException(status_code=401, detail="Unauthorized")

        user_info = retrieve_user_info(token=id_token)

        if not user_info:
            raise HTTPException(status_code=401, detail="Unauthorized")

        if not user_info.permissions >= set(permissions):
            raise HTTPException(status_code=403, detail="Forbidden")

        return user_info

    return get_user


permissions = [
    Permissions.CAN_CONNECT,
    Permissions.CAN_READ_PUBLIC,
    Permissions.CAN_MODIFY_RECORDS,
    Permissions.CAN_MODIFY_ATTRIBUTES,
    Permissions.CAN_ADD_USER,
    Permissions.CAN_ADD_OPERATOR,
    Permissions.CAN_READ_PRIVATE,
    Permissions.CAN_MODIFY_TABLES,
    Permissions.CAN_ADD_ADMIN,
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

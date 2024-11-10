from pydantic import ValidationError

from app.common.utils import DeferredModel
from ..data.repository import (
    find_user,
    get_role_permissions,
    insert_table,
    table_exists,
    insert_table_metadata,
)
from .dtos import LoginDto, CreateTableDto
from .models import UserLoginInfo
from .results import LoginResult, TableCreateResult
from .enums import Permission
from .utils.crypto import hash_password
from .utils.validation import extract_error_messages


def login(dto: DeferredModel[LoginDto]) -> LoginResult:
    try:
        login_dto = dto.validate()

        user = find_user(username=login_dto.username)

        if not user:
            return LoginResult(
                errors={"username": "Користувача з таким ім'ям не знайдено"}
            )

        hashed_password = hash_password(login_dto.password)

        if user.hashed_password != hashed_password:
            return LoginResult(errors={"password": "Неправильний пароль"})

        permissions = get_role_permissions(role_id=user.role_id)

        if Permission.CAN_CONNECT.value not in permissions:
            return LoginResult(
                errors={"username": "Користувач не має доступу до бази даних"}
            )

        login_info = UserLoginInfo(username=user.username, permissions=permissions)
        return LoginResult(login_info=login_info)

    except ValidationError as e:
        return LoginResult(errors=extract_error_messages(e))


def create_table(dto: DeferredModel[CreateTableDto]) -> TableCreateResult:
    try:
        create_table_dto = dto.validate()

        if table_exists(table_title=create_table_dto.title):
            return TableCreateResult(
                errors={"title": "Таблиця з таким ім'ям вже існує"}
            )

        insert_table(table_title=create_table_dto.title)

        table_id = insert_table_metadata(
            table_title=create_table_dto.title,
            is_private=create_table_dto.is_private,
            is_protected=create_table_dto.is_protected,
        )

        return TableCreateResult(table_id=table_id)
    except ValidationError as e:
        return TableCreateResult(errors=extract_error_messages(e))

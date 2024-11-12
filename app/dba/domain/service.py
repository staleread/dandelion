from pydantic import ValidationError

from app.common.utils.models import DeferredModel
from ..data.repository import (
    find_user,
    get_role_permissions,
    create_table_from_template,
    table_exists,
    attribute_exists,
    insert_table_metadata,
    insert_attribute_metadata,
    find_table_by_id,
    add_column_to_table,
    get_data_type_by_id,
)
from .dtos import LoginDto, CreateTableDto, AttributeCreateDto
from .models import UserLoginInfo
from .results import LoginResult, TableCreateResult, AttributeCreateResult
from ..data.models import Permission
from .utils.crypto import hash_password
from .utils.validation import extract_error_messages
from sqlalchemy.engine import Connection


def login_user(dto: DeferredModel[LoginDto], *, connection: Connection) -> LoginResult:
    try:
        login_dto = dto.validate()

        user = find_user(username=login_dto.username, connection=connection)

        if not user:
            return LoginResult(
                errors={"username": "Користувача з таким ім'ям не знайдено"}
            )

        hashed_password = hash_password(login_dto.password)

        if user.hashed_password != hashed_password:
            return LoginResult(errors={"password": "Неправильний пароль"})

        permissions = get_role_permissions(role_id=user.role_id, connection=connection)

        if Permission.CAN_CONNECT not in permissions:
            return LoginResult(
                errors={"username": "Користувач не має доступу до бази даних"}
            )

        login_info = UserLoginInfo(username=user.username, permissions=permissions)
        return LoginResult(login_info=login_info)

    except ValidationError as e:
        return LoginResult(errors=extract_error_messages(e))


def create_table(
    dto: DeferredModel[CreateTableDto], *, connection: Connection
) -> TableCreateResult:
    try:
        create_table_dto = dto.validate()

        if table_exists(table_title=create_table_dto.title, connection=connection):
            return TableCreateResult(
                errors={"title": "Таблиця з таким ім'ям вже існує"}
            )

        create_table_from_template(
            table_title=create_table_dto.title, connection=connection
        )

        table_id = insert_table_metadata(
            table_title=create_table_dto.title,
            is_private=create_table_dto.is_private,
            is_protected=create_table_dto.is_protected,
            connection=connection,
        )

        insert_attribute_metadata(
            table_id=table_id,
            name="id",
            ukr_name="ідентифікатор",
            data_type_id=1,
            is_primary=True,
            is_unique=True,
            is_nullable=False,
            connection=connection,
        )
        return TableCreateResult(table_id=table_id)

    except ValidationError as e:
        return TableCreateResult(errors=extract_error_messages(e))


def create_attribute(
    dto: DeferredModel[AttributeCreateDto], *, connection: Connection
) -> AttributeCreateResult:
    try:
        create_attr_dto = dto.validate()

        table = find_table_by_id(
            table_id=create_attr_dto.table_id, connection=connection
        )
        if not table:
            return AttributeCreateResult(errors={"table_id": "Таблиця не існує"})

        if attribute_exists(
            table_id=create_attr_dto.table_id,
            name=create_attr_dto.name,
            connection=connection,
        ):
            return AttributeCreateResult(
                errors={"name": "Атрибут з таким ім'ям вже існує"}
            )

        data_type = get_data_type_by_id(
            data_type_id=create_attr_dto.data_type_id, connection=connection
        )

        if not data_type:
            return AttributeCreateResult(
                errors={"data_type_id": "Недопустимий тип даних"}
            )

        add_column_to_table(
            table_title=table.title,
            column_name=create_attr_dto.name,
            data_type=data_type.name,
            is_nullable=create_attr_dto.is_nullable,
            connection=connection,
        )

        attribute_id = insert_attribute_metadata(
            table_id=create_attr_dto.table_id,
            name=create_attr_dto.name,
            ukr_name=create_attr_dto.ukr_name,
            data_type_id=create_attr_dto.data_type_id,
            is_primary=False,
            is_unique=create_attr_dto.is_unique,
            is_nullable=create_attr_dto.is_nullable,
            connection=connection,
        )

        return AttributeCreateResult(attribute_id=attribute_id)

    except ValidationError as e:
        return AttributeCreateResult(errors=extract_error_messages(e))

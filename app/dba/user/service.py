import bcrypt
import jwt
from datetime import datetime, timezone, timedelta
from sqlalchemy import Connection

from app.config import settings
from app.common.database.utils import SqlRunner

from .models import (
    User,
    UserLogin,
    UserTokenPayload,
    UserInfo,
    Role,
    UserAdd,
    UserReset,
)
from .enums import Permissions


def login_user(*, connection: Connection, user_login: UserLogin) -> str:
    username = _validate_username(user_login.username)
    password = _validate_password(user_login.password)

    user = _find_user(connection=connection, username=username)

    if not user:
        raise ValueError("Користувача з таким ім'ям не знайдено")

    hashed_password = _hash_password(password)

    if user.hashed_password != hashed_password:
        raise ValueError("Неправильний пароль")

    permissions = _get_role_permissions(connection=connection, role_id=user.role_id)

    if Permissions.CAN_CONNECT not in permissions:
        raise ValueError("Користувач не має доступу до бази даних")

    payload = UserTokenPayload(username=user.username, permissions=permissions)
    token = _encode_user_token(payload)

    return token


def retrieve_user_info(*, token: str) -> UserInfo | None:
    try:
        payload = _decode_user_token(token)
        return UserInfo(username=payload.username, permissions=set(payload.permissions))
    except jwt.ExpiredSignatureError:
        return None


def add_user(
    *,
    connection: Connection,
    user_add: UserAdd,
    current_user_permissions: set[Permissions],
) -> None:
    username = _validate_username(user_add.username)
    password = _validate_password(user_add.password)

    existing_user = _find_user(connection=connection, username=username)

    if existing_user:
        raise ValueError("Користувач з таким ім'ям вже існує")

    sql = SqlRunner(connection=connection)

    role = (
        sql.query("""
        select name from role where id = :role_id
    """)
        .bind(role_id=user_add.role)
        .first(lambda x: x["name"])
    )

    if not role:
        raise ValueError("Обрана роль не існує")

    if role == "guest":
        role = "user"

    if Permissions("can_add_" + role) not in current_user_permissions:
        raise ValueError(f"Ви не маєте прав для створення користувачів з роллю {role}")

    hashed_password = _hash_password(password)

    sql.query("""
        insert into "user" (username, hashed_password, role_id)
        values (:username, :password, :role_id)
    """).bind(
        username=username, password=hashed_password, role_id=user_add.role
    ).execute()


def reset_password(*, connection: Connection, user_reset: UserReset) -> None:
    username = _validate_username(user_reset.username)
    password = _validate_password(user_reset.password)

    user = _find_user(connection=connection, username=username)

    if not user:
        raise ValueError("Користувача з таким ім'ям не знайдено")

    hashed_password = _hash_password(password)

    SqlRunner(connection=connection).query("""
        update "user" set hashed_password = :hashed_password where username = :username
    """).bind(hashed_password=hashed_password, username=username).execute()


def get_available_roles(*, connection: Connection) -> list[Role]:
    return (
        SqlRunner(connection=connection)
        .query("""
            select id, name from "role"
            order by id
        """)
        .many(lambda x: Role(**x))
    )


def _validate_username(value: str | None) -> str:
    if not value:
        raise ValueError("Ім'я користувача не може бути порожнім")
    if len(value) < 3:
        raise ValueError("Ім'я користувача має містити щонайменше 3 символи")
    if len(value) > 30:
        raise ValueError("Ім'я користувача має містити не більше 30 символів")
    return value


def _validate_password(value: str | None) -> str:
    if not value:
        raise ValueError("Пароль не може бути порожнім")
    if not value.isalnum():
        raise ValueError("Пароль може містити лише літери та цифри")
    if len(value) < 3:
        raise ValueError("Пароль має містити щонайменше 3 символи")
    return value


def _find_user(*, connection: Connection, username: str) -> User | None:
    return (
        SqlRunner(connection=connection)
        .query("""
        select * from "user"
        where username = :username
    """)
        .bind(username=username)
        .first(lambda x: User(**x))
    )


def _get_role_permissions(*, connection: Connection, role_id: int) -> list[Permissions]:
    return (
        SqlRunner(connection=connection)
        .query("""
        select p.name from "role" r
        join "role_permission" rp on rp."role_id" = r.id
        join "permission" p on p.id = rp."permission_id"
        where r.id = :role_id
    """)
        .bind(role_id=role_id)
        .many(lambda x: Permissions(x["name"]))
    )


def _hash_password(password: str) -> str:
    return bcrypt.hashpw(
        password.encode("utf-8"), settings.hash_salt.encode("utf-8")
    ).decode("utf-8")


def _encode_user_token(payload: UserTokenPayload) -> str:
    data = {
        "exp": _get_timestamp_after_seconds(settings.jwt_lifetime),
        **payload.model_dump(),
    }
    return jwt.encode(data, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def _decode_user_token(token: str) -> UserTokenPayload:
    payload = jwt.decode(
        token, settings.jwt_secret, algorithms=[settings.jwt_algorithm]
    )
    return UserTokenPayload(**payload)


def _get_timestamp_after_seconds(seconds: int) -> int:
    moment = datetime.now(tz=timezone.utc) + timedelta(seconds=seconds)
    return int(moment.timestamp())

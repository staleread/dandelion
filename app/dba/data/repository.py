import pugsql  # type: ignore
from sqlalchemy import text
from app.core.engine import engine
from .models import User, Table, Attribute

queries = pugsql.module("queries/dba/")
queries.setengine(engine)


def find_user(*, username: str) -> User | None:
    result = queries.find_user(username=username)
    return User(**result) if result else None


def get_role_permissions(*, role_id: int) -> list[str]:
    return list(map(lambda x: x["name"], queries.get_role_permissions(role_id=role_id)))


def get_all_tables() -> list[Table]:
    return list(map(lambda x: Table(**x), queries.get_all_tables()))


def get_private_table(*, table_id: int) -> Table | None:
    result = queries.get_private_table(table_id=table_id)
    return Table(**result) if result else None


def get_public_table(*, table_id: int) -> Table | None:
    result = queries.get_public_table(table_id=table_id)
    return Table(**result) if result else None


def get_table(*, table_id: int) -> Table | None:
    result = queries.get_table(table_id=table_id)
    return Table(**result) if result else None


def get_table_attributes(*, table_id: int) -> list[Attribute]:
    return list(
        map(lambda x: Attribute(**x), queries.get_table_attributes(table_id=table_id))
    )


def get_attribute_columns() -> list[dict]:
    return [
        {"name": "name", "ukr_name": "назва"},
        {"name": "type", "ukr_name": "тип"},
    ]


def get_table_rows(*, table_title: str) -> list[dict]:
    with engine.connect() as connection:
        query = text(f'select * from "{table_title}"')
        result = connection.execute(query)
        return [dict(row._mapping) for row in result]


def table_exists(*, table_title: str) -> bool:
    return bool(queries.table_exists(table_title=table_title))


def insert_table(*, table_title: str):
    with engine.connect() as connection:
        query = text(f'create table "{table_title}" (id serial primary key)')
        connection.execute(query)


def insert_table_metadata(*, table_title: str, is_private: bool, is_protected: bool):
    return queries.insert_table_metadata(
        table_title=table_title,
        is_private=is_private,
        is_protected=is_protected,
    )

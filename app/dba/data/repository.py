from sqlalchemy.engine import Connection

from app.common.utils.sql_runner import SqlRunner
from .models import User, Table, Permission, DataType


def find_user(*, username: str, connection: Connection) -> User | None:
    return (
        SqlRunner(connection=connection)
        .query("""
        select * from "user" where username = :username
    """)
        .bind(username=username)
        .first(User)
    )


def get_role_permissions(*, role_id: int, connection: Connection) -> list[Permission]:
    return (
        SqlRunner(connection=connection)
        .query("""
        select p.name from "role" r
        join "role_permission" rp on rp."role_id" = r.id
        join "permission" p on p.id = rp."permission_id"
        where r.id = :role_id
    """)
        .bind(role_id=role_id)
        .many(lambda x: Permission(x["name"]))
    )


def table_exists(*, table_title: str, connection: Connection) -> bool:
    return (
        SqlRunner(connection=connection)
        .query("""
        select exists (select 1 from metadata.table where title = :table_title)
    """)
        .bind(table_title=table_title)
        .one(lambda x: x["exists"])
    )


def create_table_from_template(*, table_title: str, connection: Connection):
    return (
        SqlRunner(connection=connection)
        .query(f"""
        create table "{table_title}" (id serial primary key)
    """)
        .run_unsafe()
    )


def insert_table_metadata(
    *, table_title: str, is_private: bool, is_protected: bool, connection: Connection
):
    return (
        SqlRunner(connection=connection)
        .query("""
        insert into metadata.table (title, is_private, is_protected)
        values (:table_title, :is_private, :is_protected)
        returning id
    """)
        .bind(table_title=table_title, is_private=is_private, is_protected=is_protected)
        .one(lambda x: x["id"])
    )


def get_data_type_by_id(
    *, data_type_id: int, connection: Connection
) -> DataType | None:
    return (
        SqlRunner(connection=connection)
        .query("""
            select * from metadata.data_type 
            where id = :data_type_id
        """)
        .bind(data_type_id=data_type_id)
        .first(DataType)
    )


def find_table_by_id(*, table_id: int, connection: Connection) -> Table | None:
    return (
        SqlRunner(connection=connection)
        .query("""
            select * from metadata.table where id = :table_id
        """)
        .bind(table_id=table_id)
        .first(Table)
    )


def attribute_exists(*, table_id: int, name: str, connection: Connection) -> bool:
    return (
        SqlRunner(connection=connection)
        .query("""
            select exists (select 1 from metadata.attribute where table_id = :table_id and name = :name)
        """)
        .bind(table_id=table_id, name=name)
        .one(lambda x: x["exists"])
    )


def add_column_to_table(
    *,
    table_title: str,
    column_name: str,
    data_type: str,
    is_nullable: bool,
    connection: Connection,
):
    nullable_str = "" if is_nullable else "NOT NULL"
    return (
        SqlRunner(connection=connection)
        .query(f"""
            ALTER TABLE "{table_title}" 
            ADD COLUMN "{column_name}" {data_type} {nullable_str}
        """)
        .run_unsafe()
    )


def insert_attribute_metadata(
    *,
    table_id: int,
    name: str,
    ukr_name: str,
    data_type_id: int,
    is_primary: bool,
    is_unique: bool,
    is_nullable: bool,
    connection: Connection,
):
    return (
        SqlRunner(connection=connection)
        .query("""
        INSERT INTO metadata.attribute (
            table_id, 
            name, 
            ukr_name, 
            data_type_id,
            is_primary,
            is_unique,
            is_nullable
        )
        VALUES (
            :table_id, 
            :name, 
            :ukr_name, 
            :data_type_id,
            :is_primary,
            :is_unique,
            :is_nullable
        )
        RETURNING id
    """)
        .bind(
            table_id=table_id,
            name=name,
            ukr_name=ukr_name,
            data_type_id=data_type_id,
            is_primary=is_primary,
            is_unique=is_unique,
            is_nullable=is_nullable,
        )
        .one(lambda x: x["id"])
    )

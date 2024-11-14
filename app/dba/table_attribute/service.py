from sqlalchemy.engine import Connection
import re

from app.common.database.utils import SqlRunner

from .enums import DataTypes
from .models import Attribute, DataType, DisplayAttribute, DisplayAttributeRich


def get_all_data_types(*, connection: Connection) -> list[DataType]:
    return (
        SqlRunner(connection=connection)
        .query("""select * from metadata.data_type""")
        .many(lambda x: DataType(**x))
    )


def get_data_type_by_name(
    *, connection: Connection, data_type: DataTypes
) -> DataType | None:
    return (
        SqlRunner(connection=connection)
        .query("""select * from metadata.data_type where name = :data_type""")
        .bind(data_type=data_type.value)
        .first(lambda x: DataType(**x))
    )


def get_display_attributes(
    *, connection: Connection, table_id: int
) -> list[DisplayAttribute]:
    return (
        SqlRunner(connection=connection)
        .query("""
        select 
            a.id,
            a.table_id,
            a.name,
            a.ukr_name,
            dt.name as data_type,
            a.is_primary,
            a.is_unique,
            a.is_nullable,
            a.constraint_pattern,
            (fk.attribute_id is not null) as is_foreign
        from metadata.attribute a
        left join metadata.foreign_key fk on fk.attribute_id = a.id
        join metadata.data_type dt on dt.id = a.data_type_id
        where a.table_id = :table_id
    """)
        .bind(table_id=table_id)
        .many(lambda x: DisplayAttribute(**x))
    )


def get_rich_display_attributes(
    *, connection: Connection, table_id: int
) -> list[DisplayAttributeRich]:
    return (
        SqlRunner(connection=connection)
        .query("""
        select 
            a.id,
            a.table_id,
            a.name,
            a.ukr_name,
            dt.name as data_type,
            a.is_primary,
            a.is_unique,
            a.is_nullable,
            a.constraint_pattern,
            ft.id as foreign_table_id,
            ft.title as foreign_table_name
        from metadata.attribute a
        join metadata.data_type dt on dt.id = a.data_type_id
        left join metadata.foreign_key fk on fk.attribute_id = a.id
        left join metadata.attribute ra on ra.id = fk.referenced_attribute_id
        left join metadata.table ft on ft.id = ra.table_id
        where a.table_id = :table_id
    """)
        .bind(table_id=table_id)
        .many(lambda x: DisplayAttributeRich(**x))
    )


def insert_table_attribute(
    *,
    connection: Connection,
    table_id: int,
    table_title: str,
    name: str,
    ukr_name: str,
    data_type_id: int,
    is_unique: bool,
    is_nullable: bool,
    is_primary: bool,
    constraint_pattern: str | None = None,
):
    name = _validate_attribute_name(name)
    data_type = _find_data_type_by_id(connection=connection, data_type_id=data_type_id)

    if not data_type:
        raise ValueError("Недопустимий тип даних")

    if _attribute_exists(
        connection=connection,
        table_id=table_id,
        name=name,
    ):
        raise ValueError("Атрибут з таким ім'ям вже існує")

    if not is_nullable:
        row_count = (
            SqlRunner(connection=connection)
            .query(f'select count(*) from "{table_title}"')
            .scalar()
        )
        if row_count > 0:
            raise ValueError(
                "Неможливо додати атрибут з обов'язковим значенням до таблиці з існуючими рядками"
            )

    nullable_str = "" if is_nullable else "not null"
    unique_str = "unique" if is_unique and not is_primary else ""
    primary_str = "primary key" if is_primary else ""
    check_str = ""

    # Add check constraint if pattern is provided
    if constraint_pattern:
        if constraint_pattern.startswith("between"):
            match = re.match(r"between\s+(-?\d+)\s+and\s+(-?\d+)", constraint_pattern)
            if match:
                min_val, max_val = match.groups()
                check_str = f"check ({name} between {min_val} and {max_val})"
        elif constraint_pattern.startswith("in"):
            match = re.match(r"in\s*\(([\d\s,+-]+)\)", constraint_pattern)
            if match:
                values = match.group(1)
                check_str = f"check ({name} in ({values}))"

    SqlRunner(connection=connection).query(f"""
        alter table "{table_title}" 
        add column "{name}" {data_type.name} {nullable_str} {primary_str} {unique_str} {check_str}
    """).execute_unsafe()

    return _insert_table_attribute_metadata(
        connection=connection,
        table_id=table_id,
        name=name,
        ukr_name=ukr_name,
        data_type_id=data_type_id,
        is_primary=is_primary,
        is_unique=is_unique,
        is_nullable=is_nullable,
        constraint_pattern=constraint_pattern,
    )


def update_secondary_attribute(
    *,
    connection: Connection,
    table_title: str,
    table_id: int,
    attribute_id: int,
    old_name: str,
    new_name: str,
    new_ukr_name: str,
) -> None:
    new_name = _validate_attribute_name(new_name)

    if old_name != new_name and _attribute_exists(
        connection=connection,
        table_id=table_id,
        name=new_name,
    ):
        raise ValueError("Атрибут з таким ім'ям вже існує")

    sql = SqlRunner(connection=connection)

    if old_name != new_name:
        sql.query(f"""
            alter table "{table_title}" 
            rename column "{old_name}" to "{new_name}"
        """).execute_unsafe()

    sql.query("""
        update metadata.attribute 
        set name = :new_name, ukr_name = :new_ukr_name
        where id = :attribute_id
    """).bind(
        new_name=new_name,
        new_ukr_name=new_ukr_name,
        attribute_id=attribute_id,
    ).execute()


def find_attribute_by_id(
    *, connection: Connection, table_id: int, attribute_id: int
) -> Attribute | None:
    return (
        SqlRunner(connection=connection)
        .query("""
            select * from metadata.attribute
            where id = :attribute_id and table_id = :table_id
        """)
        .bind(attribute_id=attribute_id, table_id=table_id)
        .first(lambda x: Attribute(**x))
    )


def _validate_attribute_name(value: str) -> str:
    if not value:
        raise ValueError("Ім'я атрибута не може бути порожнім")

    if len(value) > 30:
        raise ValueError("Ім'я атрибута має містити не більше 30 символів")

    if value.startswith("_") or value.endswith("_"):
        raise ValueError(
            "Ім'я атрибута не може починатися або закінчуватися символом підкреслення"
        )

    if not all(c.isascii() and (c.islower() or c == "_") for c in value):
        raise ValueError(
            "Ім'я атрибута може містити лише малі літери англійського алфавіту та символ підкреслення"
        )

    return value


def _attribute_exists(*, connection: Connection, table_id: int, name: str) -> bool:
    return (
        SqlRunner(connection=connection)
        .query("""
            select exists (select 1 from metadata.attribute where table_id = :table_id and name = :name)
        """)
        .bind(table_id=table_id, name=name)
        .scalar()
    )


def _find_data_type_by_id(
    *, connection: Connection, data_type_id: int
) -> DataType | None:
    return (
        SqlRunner(connection=connection)
        .query("""
            select * from metadata.data_type where id = :data_type_id
        """)
        .bind(data_type_id=data_type_id)
        .first(lambda x: DataType(**x))
    )


def _insert_table_attribute_metadata(
    *,
    connection: Connection,
    table_id: int,
    name: str,
    ukr_name: str,
    data_type_id: int,
    is_primary: bool,
    is_unique: bool,
    is_nullable: bool,
    constraint_pattern: str | None = None,
):
    return (
        SqlRunner(connection=connection)
        .query("""
        insert into metadata.attribute (
            table_id, 
            name, 
            ukr_name, 
            data_type_id,
            is_primary,
            is_unique,
            is_nullable,
            constraint_pattern
        )
        values (
            :table_id, 
            :name, 
            :ukr_name, 
            :data_type_id,
            :is_primary,
            :is_unique,
            :is_nullable,
            :constraint_pattern
        )
        returning id
    """)
        .bind(
            table_id=table_id,
            name=name,
            ukr_name=ukr_name,
            data_type_id=data_type_id,
            is_primary=is_primary,
            is_unique=is_unique,
            is_nullable=is_nullable,
            constraint_pattern=constraint_pattern,
        )
        .scalar()
    )

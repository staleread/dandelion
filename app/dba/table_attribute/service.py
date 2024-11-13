from sqlalchemy.engine import Connection

from app.common.database.utils import SqlRunner

from .enums import DataTypes
from .models import Attribute, DataType, AttributeRich


def get_all_data_types(*, connection: Connection) -> list[DataType]:
    return (
        SqlRunner(connection=connection)
        .query("""select * from metadata.data_type""")
        .all(DataType)
    )


def get_data_type_by_name(
    *, connection: Connection, data_type: DataTypes
) -> DataType | None:
    return (
        SqlRunner(connection=connection)
        .query("""select * from metadata.data_type where name = :data_type""")
        .bind(data_type=data_type.value)
        .first(DataType)
    )


def get_table_attributes(*, connection: Connection, table_id: int) -> list[Attribute]:
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
            (fk.attribute_id is not null) as is_foreign
        from metadata.attribute a
        left join metadata.foreign_key fk on fk.attribute_id = a.id
        join metadata.data_type dt on dt.id = a.data_type_id
        where a.table_id = :table_id
    """)
        .bind(table_id=table_id)
        .all(Attribute)
    )


def get_table_rich_attributes(
    *, connection: Connection, table_id: int
) -> list[AttributeRich]:
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
        .all(AttributeRich)
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

    nullable_str = "" if is_nullable else "not null"
    unique_str = "unique" if is_unique and not is_primary else ""
    primary_str = "primary key" if is_primary else ""

    SqlRunner(connection=connection).query(f"""
        alter table "{table_title}" 
        add column "{name}" {data_type.name} {nullable_str} {primary_str} {unique_str} 
    """).run_unsafe()

    return _insert_table_attribute_metadata(
        connection=connection,
        table_id=table_id,
        name=name,
        ukr_name=ukr_name,
        data_type_id=data_type_id,
        is_primary=is_primary,
        is_unique=is_unique,
        is_nullable=is_nullable,
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

    if not all(c.islower() or c == "_" for c in value):
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
        .map_one(lambda x: x["exists"])
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
        .first(DataType)
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
            is_nullable
        )
        values (
            :table_id, 
            :name, 
            :ukr_name, 
            :data_type_id,
            :is_primary,
            :is_unique,
            :is_nullable
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
        )
        .map_one(lambda x: x["id"])
    )

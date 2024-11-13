from sqlalchemy.engine import Connection

from app.common.exceptions import ValidationException
from app.common.database.utils import SqlRunner

from ..table_attribute.enums import DataTypes
from ..table_attribute.service import insert_table_attribute, get_data_type_by_name
from .models import TableCreate, Table, AttributeSecondaryCreate


def find_table_by_id(*, connection: Connection, table_id: int) -> Table | None:
    return (
        SqlRunner(connection=connection)
        .query("""
            select * from metadata.table
            where id = :table_id
        """)
        .bind(table_id=table_id)
        .first(Table)
    )


def create_table(*, connection: Connection, table_create: TableCreate):
    table_title = _validate_table_title(value=table_create.title)

    if _table_exists(table_title=table_title, connection=connection):
        raise ValidationException(
            source="title", message="Таблиця з таким ім'ям вже існує"
        )

    _create_empty_table(table_title=table_title, connection=connection)

    table_id = _insert_table_metadata(
        table_title=table_title,
        is_private=table_create.is_private,
        is_protected=table_create.is_protected,
        connection=connection,
    )

    data_type = get_data_type_by_name(connection=connection, data_type=DataTypes.SERIAL)

    if not data_type:
        raise ValueError("Cannot find data type for primary key")

    insert_table_attribute(
        connection=connection,
        table_id=table_id,
        table_title=table_title,
        name="id",
        ukr_name="ID",
        data_type_id=data_type.id,
        is_unique=True,
        is_nullable=False,
        is_primary=True,
    )


def create_secondary_table_attribute(
    *, connection: Connection, attribute_create: AttributeSecondaryCreate
):
    IS_PRIMARY = False

    table = find_table_by_id(connection=connection, table_id=attribute_create.table_id)

    if not table:
        raise ValidationException(source="table_id", message="Таблиця не існує")

    insert_table_attribute(
        connection=connection,
        table_id=attribute_create.table_id,
        table_title=table.title,
        name=attribute_create.name,
        ukr_name=attribute_create.ukr_name,
        data_type_id=attribute_create.data_type_id,
        is_unique=attribute_create.is_unique,
        is_nullable=attribute_create.is_nullable,
        is_primary=IS_PRIMARY,
    )


def _validate_table_title(*, value: str) -> str:
    if not value:
        raise ValidationException(
            source="title", message="Ім'я таблиці не може бути порожнім"
        )

    if len(value) < 3:
        raise ValidationException(
            source="title", message="Ім'я таблиці повинно містити щонайменше 3 символи"
        )

    if len(value) > 30:
        raise ValidationException(
            source="title", message="Ім'я таблиці повинно містити не більше 30 символів"
        )

    if value.startswith("_") or value.endswith("_"):
        raise ValidationException(
            source="title",
            message="Ім'я таблиці не може починатися або закінчуватися символом підкреслення",
        )

    if not all(c.islower() or c == "_" for c in value):
        raise ValidationException(
            source="title",
            message="Ім'я таблиці може містити лише малі літери англійського алфавіту та символ підкреслення",
        )

    return value


def _table_exists(*, table_title: str, connection: Connection) -> bool:
    return (
        SqlRunner(connection=connection)
        .query("""
            select exists (
                select 1 from information_schema.tables 
                where table_name = :table_title
            )
        """)
        .bind(table_title=table_title)
        .map_one(lambda x: x["exists"])
    )


def _create_empty_table(*, table_title: str, connection: Connection) -> None:
    SqlRunner(connection=connection).query(f"""
        create table "{table_title}" ()
    """).run_unsafe()


def _insert_table_metadata(
    *, connection: Connection, table_title: str, is_private: bool, is_protected: bool
) -> int:
    return (
        SqlRunner(connection=connection)
        .query("""
        insert into metadata.table (title, is_private, is_protected)
        values (:table_title, :is_private, :is_protected)
        returning id
    """)
        .bind(table_title=table_title, is_private=is_private, is_protected=is_protected)
        .map_one(lambda x: x["id"])
    )

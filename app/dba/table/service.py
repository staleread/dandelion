from typing import Any
from sqlalchemy.engine import Connection
from datetime import datetime, date
import re
from json import loads, dumps

from app.common.database.utils import SqlRunner

from ..table_attribute.models import Attribute, DisplayAttribute
from ..table_attribute.enums import DataTypes
from ..table_attribute.service import (
    insert_table_attribute,
    get_data_type_by_name,
    get_display_attributes,
    update_secondary_attribute,
    find_attribute_by_id,
    delete_attribute,
)
from ..table_row.service import (
    get_table_rows,
    delete_row_by_id,
    update_row_by_id,
    insert_row,
)
from .models import TableCreate, Table, AttributeSecondaryCreate


def find_table_by_id(*, connection: Connection, table_id: int) -> Table | None:
    return (
        SqlRunner(connection=connection)
        .query("""
            select * from metadata.table
            where id = :table_id
        """)
        .bind(table_id=table_id)
        .first(lambda x: Table(**x))
    )


def create_table(*, connection: Connection, table_create: TableCreate):
    table_title = _validate_table_title(value=table_create.title)

    if _table_exists(table_title=table_title, connection=connection):
        raise ValueError("Таблиця з таким ім'ям вже існує")

    _create_empty_table(table_title=table_title, connection=connection)

    table_id = _insert_table_metadata(
        table_title=table_title,
        is_private=table_create.is_private,
        is_protected=table_create.is_protected,
        connection=connection,
    )

    data_type = get_data_type_by_name(connection=connection, data_type=DataTypes.SERIAL)

    if not data_type:
        raise RuntimeError("Cannot find data type for primary key")

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
        raise ValueError("Таблиця не існує")

    data_type = get_data_type_by_name(
        connection=connection, data_type=DataTypes.INTEGER
    )

    if not data_type:
        raise ValueError("Не вдалося знайти тип даних для нової колонки")

    try:
        constraint = _parse_constraint_pattern(
            data_type=data_type.name, pattern=attribute_create.constraint_pattern
        )
    except ValueError as e:
        raise ValueError(f"Помилка в обмеженні: {str(e)}")

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
        constraint_pattern=constraint,
    )


def edit_secondary_table_attribute(
    *,
    connection: Connection,
    table_id: int,
    attribute_id: int,
    name: str,
    ukr_name: str,
) -> None:
    table = find_table_by_id(connection=connection, table_id=table_id)
    if not table:
        raise ValueError("Таблиця не існує")

    attribute = (
        SqlRunner(connection=connection)
        .query("""
            select * from metadata.attribute
            where id = :attribute_id and table_id = :table_id
        """)
        .bind(attribute_id=attribute_id, table_id=table_id)
        .first(lambda x: Attribute(**x))
    )

    if not attribute:
        raise ValueError("Атрибут не існує")

    if attribute.is_primary:
        raise ValueError("Не можна редагувати первинний ключ")

    update_secondary_attribute(
        connection=connection,
        table_title=table.title,
        table_id=table_id,
        attribute_id=attribute_id,
        old_name=attribute.name,
        new_name=name,
        new_ukr_name=ukr_name,
    )


def delete_table_attribute(
    *, connection: Connection, table_id: int, attribute_id: int
) -> None:
    table = find_table_by_id(connection=connection, table_id=table_id)
    if not table:
        raise ValueError("Таблиця не існує")

    attribute = find_attribute_by_id(
        connection=connection,
        table_id=table_id,
        attribute_id=attribute_id,
    )

    if not attribute:
        raise ValueError("Атрибут не існує")

    if attribute.is_primary:
        raise ValueError("Не можна видалити первинний ключ")

    delete_attribute(
        connection=connection,
        table_title=table.title,
        attribute_id=attribute_id,
        attribute_name=attribute.name,
    )


def delete_table(*, connection: Connection, table_id: int) -> None:
    table = find_table_by_id(connection=connection, table_id=table_id)

    if not table:
        raise ValueError("Таблиця не існує")

    if table.is_protected:
        raise ValueError("Захищену таблицю не можна видалити")

    sql = SqlRunner(connection=connection)

    sql.query(f"""
        drop table if exists "{table.title}"
    """).execute_unsafe()

    sql.query("""
        delete from metadata.table where id = :table_id
    """).bind(table_id=table_id).execute()


def get_formatted_table_rows(
    *, connection: Connection, table_title: str, attributes: list[DisplayAttribute]
) -> list[dict]:
    rows = get_table_rows(connection=connection, table_title=table_title)
    attr_map = {attr.name: attr for attr in attributes}

    formatted_rows = []
    for row in rows:
        formatted_row = {}
        for key, value in row.items():
            attr = attr_map.get(key)

            if not attr:
                formatted_row[key] = str(value)
                continue

            if attr.data_type == DataTypes.JSON.value:
                try:
                    # Parse and prettify JSON with 2-space indentation
                    if isinstance(value, str):
                        parsed_json = loads(value)
                    else:
                        parsed_json = value
                    formatted_row[key] = dumps(
                        parsed_json, ensure_ascii=False, indent=2
                    )
                except (ValueError, TypeError):
                    formatted_row[key] = str(value)  # Fallback if JSON parsing fails
                continue

            if attr.data_type == DataTypes.TIMESTAMP.value:
                formatted_row[key] = value.isoformat()
                continue

            if attr.data_type == DataTypes.TIME.value:
                formatted_row[key] = value.strftime("%H:%M:%S")
                continue

            if attr.data_type == DataTypes.DATE.value:
                formatted_row[key] = value.strftime("%Y-%m-%d")
                continue

            formatted_row[key] = str(value)

        formatted_rows.append(formatted_row)

    return formatted_rows


def add_row(*, connection: Connection, table_id: int, values: dict[str, Any]) -> None:
    table = find_table_by_id(connection=connection, table_id=table_id)

    if not table:
        raise ValueError("Таблиця не існує")

    attributes = get_display_attributes(connection=connection, table_id=table.id)

    _validate_row(
        connection=connection,
        table=table,
        attributes=attributes,
        values=values,
        exclude_current=False,
    )

    _convert_values_to_db_format(values=values, attributes=attributes)

    insert_row(
        connection=connection,
        table_title=table.title,
        values=values,
    )


def update_row(
    *, connection: Connection, table_id: int, row_id: int, values: dict[str, Any]
) -> None:
    table = find_table_by_id(connection=connection, table_id=table_id)

    if not table:
        raise ValueError("Таблиця не існує")

    attributes = get_display_attributes(connection=connection, table_id=table.id)

    _validate_row(
        connection=connection,
        table=table,
        attributes=attributes,
        values=values,
        exclude_current=True,
    )

    update_row_by_id(
        connection=connection,
        table_title=table.title,
        row_id=row_id,
        values=values,
    )


def delete_row(*, connection: Connection, table_id: int, row_id: int) -> None:
    table = find_table_by_id(connection=connection, table_id=table_id)
    if not table:
        raise ValueError("Таблиця не існує")

    delete_row_by_id(
        connection=connection,
        table_title=table.title,
        row_id=row_id,
    )


def _validate_row(
    *,
    connection: Connection,
    table: Table,
    attributes: list[DisplayAttribute],
    values: dict[str, Any],
    exclude_current: bool = False,
) -> None:
    sql = SqlRunner(connection=connection)

    primary_attrs = [a for a in attributes if a.is_primary]
    secondary_attrs = [a for a in attributes if not a.is_primary]

    # Validate no unknown columns are being inserted
    valid_columns = {a.name for a in attributes}
    unknown_columns = set(values.keys()) - valid_columns
    if unknown_columns:
        raise ValueError(f"Неіснуючі колонки: {', '.join(unknown_columns)}")

    # Check composite primary key constraints
    if len(primary_attrs) > 1:
        if len(secondary_attrs) > 0:
            raise RuntimeError(
                "Композитний первинний ключ підтримується лише для ��аблиць, що допомагають встановити багато-до-багато відношення"
            )

        check_pk = " and ".join(f"{a.name} = :{a.name}" for a in primary_attrs)
        is_duplicate = (
            sql.query(f"""
            select exists (
                select 1 from "{table.title}" 
                where {check_pk}
            )
        """)
            .bind(**values)
            .scalar()
        )

        if is_duplicate:
            raise ValueError("Цей рядок вже існує")

    # Check required fields
    for attr in secondary_attrs:
        if (
            not attr.is_nullable
            and attr.name not in values
            and attr.data_type != "serial"
        ):
            raise ValueError(f"{attr.ukr_name}: Це поле є обов'язковим")

    # Check unique constraints
    for attr in (a for a in secondary_attrs if a.is_unique):
        if attr.name not in values:
            continue

        bind_params = {"value": values[attr.name]}

        if exclude_current:
            bind_params["exclude_id"] = values["id"]

        is_duplicate = (
            sql.query(f"""
            select exists (
                select 1 from "{table.title}" 
                where {attr.name} = :value
                {"and id != :exclude_id" if exclude_current else ""}
            )
        """)
            .bind(**bind_params)
            .scalar()
        )

        if is_duplicate:
            raise ValueError(f"{attr.ukr_name}: Це значення повинно бути унікальним")

    # Check foreign key constraints
    for attr in secondary_attrs:
        if attr.name not in values or values[attr.name] is None:
            continue

        fk_relation = (
            sql.query("""
                select 
                    ft.title as foreign_table,
                    fa.name as foreign_column
                from metadata.foreign_key fk
                join metadata.attribute ta on ta.id = fk.attribute_id
                join metadata.attribute fa on fa.id = fk.referenced_attribute_id
                join metadata.table ft on ft.id = fa.table_id
                where ta.table_id = :table_id and ta.name = :attr_name
            """)
            .bind(table_id=table.id, attr_name=attr.name)
            .first_row()
        )

        if fk_relation:
            exists = (
                sql.query(f"""
                    select exists (
                        select 1 from "{fk_relation['foreign_table']}"
                        where id = :value
                    )
                """)
                .bind(value=values[attr.name])
                .scalar()
            )
            if not exists:
                raise ValueError(
                    f"{attr.ukr_name}: Вказане значення не існує у цільовій таблиці"
                )

    # Add constraint validation
    for attr in attributes:
        if attr.name not in values or values[attr.name] is None:
            continue

        if attr.data_type == DataTypes.INTEGER.value and attr.constraint_pattern:
            value = values[attr.name]
            try:
                value = int(value)
            except ValueError:
                raise ValueError(f"{attr.ukr_name}: Значення має бути цілим числом")

            if attr.constraint_pattern.startswith("between"):
                match = re.match(
                    r"between\s+(-?\d+)\s+and\s+(-?\d+)", attr.constraint_pattern
                )
                if match:
                    min_val, max_val = map(int, match.groups())
                    if not (min_val <= value <= max_val):
                        raise ValueError(
                            f"{attr.ukr_name}: Значення має бути між {min_val} та {max_val}"
                        )

            elif attr.constraint_pattern.startswith("in"):
                match = re.match(r"in\s*\(([\d\s,+-]+)\)", attr.constraint_pattern)
                if match:
                    allowed_values = [int(x.strip()) for x in match.group(1).split(",")]
                    if value not in allowed_values:
                        raise ValueError(
                            f"{attr.ukr_name}: Значення має бути одним з: {', '.join(map(str, allowed_values))}"
                        )


def _validate_table_title(*, value: str) -> str:
    if not value:
        raise ValueError("Ім'я таблиці не може бути порожнім")

    if len(value) < 3:
        raise ValueError("Ім'я таблиці повинно містити щонайменше 3 символи")

    if len(value) > 30:
        raise ValueError("Ім'я таблиці повинно містити не більше 30 символів")

    if value.startswith("_") or value.endswith("_"):
        raise ValueError(
            "Ім'я таблиці не може починатися або закінчуватися символом підкреслення"
        )

    if not all(c.islower() or c == "_" for c in value):
        raise ValueError(
            "Ім'я таблиці може містити лише малі літери англійського алфавіту та символ підкрслення"
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
        .scalar()
    )


def _create_empty_table(*, table_title: str, connection: Connection) -> None:
    SqlRunner(connection=connection).query(f"""
        create table "{table_title}" ()
    """).execute_unsafe()


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
        .scalar()
    )


def _convert_values_to_db_format(
    *, values: dict[str, Any], attributes: list[DisplayAttribute]
) -> None:
    attr_map = {attr.name: attr for attr in attributes}

    for key, value in values.items():
        if value is None:
            continue

        attr = attr_map.get(key)
        if not attr:
            continue

        if isinstance(value, str):
            if attr.data_type == DataTypes.JSON.value:
                try:
                    parsed_json = loads(value)
                    values[key] = dumps(parsed_json, ensure_ascii=False)
                except ValueError:
                    raise ValueError(f"{attr.ukr_name}: Неправильний формат JSON")

            elif attr.data_type == DataTypes.TIMESTAMP.value:
                try:
                    values[key] = datetime.fromisoformat(value.replace("Z", "+00:00"))
                except ValueError:
                    raise ValueError(
                        f"{attr.ukr_name}: Неправильний формат дати та часу"
                    )

            elif attr.data_type == DataTypes.DATE.value:
                try:
                    values[key] = date.fromisoformat(value)
                except ValueError:
                    raise ValueError(f"{attr.ukr_name}: Неправильний формат дати")


def _parse_constraint_pattern(data_type: str, pattern: str | None) -> str | None:
    if not pattern or not pattern.strip() or data_type != DataTypes.INTEGER.value:
        return None

    pattern = pattern.strip().lower()

    # Parse "between X and Y"
    between_match = re.match(r"^between\s+(-?\d+)\s+and\s+(-?\d+)$", pattern)
    if between_match:
        start, end = map(int, between_match.groups())
        if start >= end:
            raise ValueError("В обмеженні 'between' перше число має бути менше другого")
        return f"between {start} and {end}"

    # Parse "in (X, Y, ...)"
    in_match = re.match(r"^in\s*\(([\d\s,+-]+)\)$", pattern)
    if in_match:
        try:
            values = [int(x.strip()) for x in in_match.group(1).split(",")]
            if not values:
                raise ValueError()
            return f"in ({', '.join(map(str, values))})"
        except ValueError:
            raise ValueError(
                "Обмеження 'in' має містити список цілих чисел, розділених комами"
            )

    raise ValueError(
        "Підтримуються лише обмеження типу 'between X and Y' та 'in (X, Y, ...)'"
    )

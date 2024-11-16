from sqlalchemy.engine import Connection

from app.common.database.utils import SqlRunner


def get_table_rows(*, connection: Connection, table_title: str) -> list[dict]:
    return (
        SqlRunner(connection=connection)
        .query(f"""
            select * from "{table_title}"
        """)
        .many_rows()
    )


def get_row_by_id(
    *, connection: Connection, table_title: str, row_id: int
) -> dict | None:
    return (
        SqlRunner(connection=connection)
        .query(f"SELECT * FROM {table_title} WHERE id = :row_id")
        .bind(row_id=row_id)
        .first_row()
    )


def insert_row(*, connection: Connection, table_title: str, values: dict) -> None:
    sql = SqlRunner(connection=connection)

    columns = ", ".join(values.keys())
    placeholders = ", ".join(f":{k}" for k in values.keys())

    sql.query(f"""
        insert into "{table_title}" ({columns})
        values ({placeholders})
    """).bind(**values).execute()


def update_row_by_id(
    *, connection: Connection, table_title: str, row_id: int, values: dict
) -> None:
    sql = SqlRunner(connection=connection)

    placeholders = ", ".join(f"{k} = :{k}" for k in values.keys())

    sql.query(f"""
        update "{table_title}" set {placeholders}
        where id = :row_id
    """).bind(**{k: v for k, v in values.items() if k != "id"}, row_id=row_id).execute()


def delete_row_by_id(*, connection: Connection, table_title: str, row_id: int) -> None:
    row_exists = (
        SqlRunner(connection=connection)
        .query(f"""
            select exists (
                select 1 from "{table_title}"
                where id = :row_id
            )
        """)
        .bind(row_id=row_id)
        .scalar()
    )

    if not row_exists:
        raise ValueError("Рядок не існує")

    SqlRunner(connection=connection).query(f"""
        delete from "{table_title}"
        where id = :row_id
    """).bind(row_id=row_id).execute()

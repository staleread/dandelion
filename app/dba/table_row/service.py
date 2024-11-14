from sqlalchemy.engine import Connection

from app.common.database.utils import SqlRunner


def get_table_rows(*, connection: Connection, table_title: str) -> list[dict]:
    return (
        SqlRunner(connection=connection)
        .query(f'select * from "{table_title}"')
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

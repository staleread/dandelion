from sqlalchemy.engine import Connection

from app.common.database.utils import SqlRunner


def get_table_rows(*, connection: Connection, table_title: str) -> list[dict]:
    return SqlRunner(connection=connection).query(f"select * from {table_title}").many()

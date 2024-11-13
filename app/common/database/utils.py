from typing import Annotated
from fastapi import Depends
from sqlalchemy import text
from sqlalchemy.engine import Connection
from sqlalchemy.engine.row import RowMapping
from typing import TypeVar, Callable, Any, Type

from .core import engine


T = TypeVar("T")


class SqlQueryRunner:
    def __init__(self, *, connection: Connection):
        self.connection = connection
        self.kwargs: dict[str, Any] = {}

    def query(self, sql: str):
        self.sql = sql
        return self

    def bind(self, **kwargs: str | int | float | bool):
        self.kwargs = kwargs
        return self

    def first(self, type: Type[T]) -> T | None:
        if not self.sql:
            raise ValueError("sql is not set")

        row = self.connection.execute(text(self.sql), self.kwargs).first()
        return type(**dict(row._mapping)) if row else None

    def one(self) -> dict:
        if not self.sql:
            raise ValueError("sql is not set")

        row = self.connection.execute(text(self.sql), self.kwargs).one()

        if not row:
            raise ValueError("no row found")

        return dict(row._mapping)

    def map_one(self, map_row: Callable[[RowMapping], T]) -> T:
        if not self.sql:
            raise ValueError("sql is not set")

        row = self.connection.execute(text(self.sql), self.kwargs).one()

        if not row:
            raise ValueError("no row found")

        return map_row(row._mapping)

    def all(self, type: Type[T]) -> list[T]:
        if not self.sql:
            raise ValueError("sql is not set")

        rows = self.connection.execute(text(self.sql), self.kwargs).all()
        return list(map(lambda x: type(**dict(x._mapping)), rows))

    def many(self) -> list[dict]:
        if not self.sql:
            raise ValueError("sql is not set")

        rows = self.connection.execute(text(self.sql), self.kwargs).all()
        return list(map(lambda x: dict(x._mapping), rows))

    def map_many(self, map_row: Callable[[RowMapping], T]) -> list[T]:
        if not self.sql:
            raise ValueError("sql is not set")

        rows = self.connection.execute(text(self.sql), self.kwargs).all()
        return list(map(lambda x: map_row(x._mapping), rows))


class SqlRunner(SqlQueryRunner):
    def __init__(self, *, connection: Connection):
        super().__init__(connection=connection)

    def run(self):
        if not self.sql:
            raise ValueError("sql is not set")

        self.connection.execute(text(self.sql), self.kwargs)

    def run_unsafe(self):
        if not self.sql:
            raise ValueError("sql is not set")

        self.connection.exec_driver_sql(self.sql, self.kwargs)


def get_connection():
    with engine.begin() as connection:
        yield connection


ConnectionDep = Annotated[Connection, Depends(get_connection)]


def get_query_runner(connection: ConnectionDep) -> SqlQueryRunner:
    return SqlQueryRunner(connection=connection)


QueryRunnerDep = Annotated[SqlQueryRunner, Depends(get_query_runner)]

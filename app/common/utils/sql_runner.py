from sqlalchemy import text
from sqlalchemy.engine import Connection
from typing import TypeVar, Callable, Any, Type

T = TypeVar("T")


class SqlRunner:
    def __init__(self, *, connection: Connection):
        self.connection = connection
        self.kwargs: dict[str, Any] = {}

    def query(self, sql: str):
        self.sql = sql
        return self

    def bind(self, **kwargs: dict[str, Any]):
        self.kwargs = kwargs
        return self

    def first(self, type: Type[T]) -> T | None:
        if not self.sql:
            raise ValueError("sql is not set")

        row = self.connection.execute(text(self.sql), self.kwargs).first()
        return type(**row._mapping) if row else None

    def one(self, map_dict: Callable[[dict], Any] | None = None) -> Any | None:
        if not self.sql:
            raise ValueError("sql is not set")

        row = self.connection.execute(text(self.sql), self.kwargs).one()
        return map_dict(row._mapping) if map_dict and row else row  # type: ignore

    def all(self, type: Type[T]) -> list[T]:
        if not self.sql:
            raise ValueError("sql is not set")

        rows = self.connection.execute(text(self.sql), self.kwargs).all()
        return list(map(lambda x: type(**x._mapping), rows))

    def many(self, map_dict: Callable[[dict], Any] | None = None) -> list[Any]:
        if not self.sql:
            raise ValueError("sql is not set")

        rows = self.connection.execute(text(self.sql), self.kwargs).all()
        return list(
            map(lambda x: map_dict(x._mapping) if map_dict else x._mapping, rows)  # type: ignore
        )

    def run(self):
        if not self.sql:
            raise ValueError("sql is not set")

        self.connection.execute(text(self.sql), self.kwargs)

    def run_unsafe(self):
        if not self.sql:
            raise ValueError("sql is not set")

        self.connection.exec_driver_sql(self.sql, self.kwargs)

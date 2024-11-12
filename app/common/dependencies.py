from typing import Annotated
from sqlalchemy.engine import Connection
from fastapi import Depends
from app.core.engine import engine
from .utils.sql_runner import SqlRunner


def get_connection():
    with engine.begin() as connection:
        yield connection


ConnectionDep = Annotated[Connection, Depends(get_connection)]


def get_sql_runner(connection: ConnectionDep) -> SqlRunner:
    return SqlRunner(connection=connection)


SqlRunnerDep = Annotated[SqlRunner, Depends(get_sql_runner)]

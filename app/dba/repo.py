import pugsql  # type: ignore

from app.core.engine import engine

repo = pugsql.module("queries/dba/")
repo.setengine(engine)

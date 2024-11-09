from pydantic import ValidationError
from app.core.engine import engine
from sqlalchemy import text


def extract_error_messages(e: ValidationError) -> dict:
    error_dict = {}
    for error in e.errors():
        field = str(error["loc"][0])
        message = error["msg"]
        if field not in error_dict:
            error_dict[field + "_error"] = message
    return error_dict


def get_rows_from_table(table_name: str) -> list[dict]:
    with engine.connect() as connection:
        query = text(f'select * from "{table_name}"')
        result = connection.execute(query)
        return [dict(row._mapping) for row in result]

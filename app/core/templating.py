from fastapi import Request
from fastapi.templating import Jinja2Templates


def set_schema(request: Request) -> dict:
    schema = "dba" if request.url.path.startswith("/db") else "classic"
    return {"schema": schema}


directory = "templates/web"

templates = Jinja2Templates(directory=directory, context_processors=[set_schema])

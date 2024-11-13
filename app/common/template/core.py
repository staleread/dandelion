from fastapi import Request
from fastapi.templating import Jinja2Templates


def set_schema(request: Request) -> dict:
    schema = "dba" if request.url.path.startswith("/db") else "classic"
    return {"schema": schema}


templates = Jinja2Templates(directory="templates/web", context_processors=[set_schema])

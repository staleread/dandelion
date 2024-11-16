from fastapi import Request
from fastapi.templating import Jinja2Templates
from jinja2 import Environment, FileSystemLoader
import os


def set_schema(request: Request) -> dict:
    schema = "dba" if request.url.path.startswith("/dba") else "classic"
    return {"schema": schema}


web_templates = Jinja2Templates(
    directory="templates/web", context_processors=[set_schema]
)


def create_pdf_env():
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
    template_dir = os.path.join(project_root, "templates")

    env = Environment(
        loader=FileSystemLoader(template_dir),
        autoescape=True,
    )

    return env


pdf_templates = create_pdf_env()

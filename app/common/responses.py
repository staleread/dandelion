from fastapi import Request
from pydantic import BaseModel

from app.core.templating import templates


def template_response(
    request: Request, template: str, context: BaseModel | None = None
):
    return templates.TemplateResponse(
        request, name=template, context=context.model_dump() if context else {}
    )


def internal_error_response(request: Request):
    return template_response(request, "common/errors/500.html")


def forbidden_error_response(request: Request):
    return template_response(request, "common/errors/403.html")


def not_found_error_response(request: Request):
    return template_response(request, "common/errors/404.html")

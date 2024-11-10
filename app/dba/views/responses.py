from fastapi import Request
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

from app.core.templating import templates
from .enums import DbaTemplate
from .page_contexts import (
    LoginPageContext,
    HomePageContext,
    TablesViewContext,
    TableRowsContext,
    TableAttributesContext,
    TableCreateContext,
)


def anonymous_user_redirect():
    return RedirectResponse(url="/db/login", status_code=302)


def template_response(
    request: Request, template: DbaTemplate, context: BaseModel | None = None
):
    return templates.TemplateResponse(
        request, name=template.value, context=context.model_dump() if context else {}
    )


def login_page_response(request: Request, context: LoginPageContext):
    return template_response(request, DbaTemplate.LOGIN, context)


def home_page_response(request: Request, context: HomePageContext):
    return template_response(request, DbaTemplate.HOME, context)


def tables_view_response(request: Request, context: TablesViewContext):
    return template_response(request, DbaTemplate.TABLES, context)


def table_rows_response(request: Request, context: TableRowsContext):
    return template_response(request, DbaTemplate.TABLE_ROWS, context)


def table_attributes_response(request: Request, context: TableAttributesContext):
    return template_response(request, DbaTemplate.TABLE_ATTRIBUTES, context)


def table_create_response(request: Request, context: TableCreateContext):
    return template_response(request, DbaTemplate.TABLE_NEW, context)


def attribute_create_response(request: Request):
    return template_response(request, DbaTemplate.ATTRIBUTE_NEW)


def internal_error_response(request: Request):
    return template_response(request, DbaTemplate.INTERNAL_ERROR)


def unauthorized_error_response(request: Request):
    return template_response(request, DbaTemplate.UNAUTHORIZED_ERROR)


def not_found_error_response(request: Request):
    return template_response(request, DbaTemplate.NOT_FOUND_ERROR)

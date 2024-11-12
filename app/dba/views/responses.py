from fastapi import Request
from fastapi.responses import RedirectResponse

from app.common.responses import template_response
from .page_contexts import (
    LoginPageContext,
    HomePageContext,
    TablesViewContext,
    TableRowsContext,
    TableAttributesContext,
    TableCreateContext,
    AttributeCreateContext,
)


def unauthorized_user_redirect():
    return RedirectResponse(url="/db/login", status_code=302)


def login_page_response(request: Request, context: LoginPageContext):
    return template_response(request, "dba/login.html", context)


def home_page_response(request: Request, context: HomePageContext):
    return template_response(request, "dba/home.html", context)


def tables_view_response(request: Request, context: TablesViewContext):
    return template_response(request, "dba/tables.html", context)


def table_rows_response(request: Request, context: TableRowsContext):
    return template_response(request, "dba/table_rows.html", context)


def table_attributes_response(request: Request, context: TableAttributesContext):
    return template_response(request, "dba/table_attributes.html", context)


def table_create_response(request: Request, context: TableCreateContext):
    return template_response(request, "dba/table_new.html", context)


def attribute_create_response(request: Request, context: AttributeCreateContext):
    return template_response(request, "dba/attribute_new.html", context)

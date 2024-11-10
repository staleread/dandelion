from typing import Annotated
from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import RedirectResponse

from ..domain.dtos import LoginDto, CreateTableDto
from ..domain.service import login, create_table
from .utils.jwt import encode_user_login_info
from .dependencies import Guest, Owner
from .page_contexts import (
    LoginPageContext,
    HomePageContext,
    TablesViewContext,
    TableRowsContext,
    TableAttributesContext,
    TableCreateContext,
)
from .responses import (
    anonymous_user_redirect,
    not_found_error_response,
    login_page_response,
    home_page_response,
    tables_view_response,
    table_rows_response,
    table_attributes_response,
    table_create_response,
)
from ..data.repository import (
    get_all_tables,
    get_private_table,
    get_public_table,
    get_table,
    get_table_attributes,
    get_attribute_columns,
    get_table_rows,
)


router = APIRouter(prefix="/db")


@router.get("/")
async def home_page(request: Request, user: Guest):
    if not user:
        return anonymous_user_redirect()

    if not user.is_authorized:
        raise HTTPException(status_code=401)

    return home_page_response(request, HomePageContext(username=user.username))


@router.get("/login")
async def login_page(request: Request, user: Guest):
    if user and user.is_authorized:
        return anonymous_user_redirect()

    return login_page_response(request, LoginPageContext())


@router.post("/login")
async def handle_login(
    request: Request,
    username: Annotated[str | None, Form()],
    password: Annotated[str | None, Form()],
):
    dto = LoginDto.defer(username=username, password=password)
    result = login(dto)

    if result.errors:
        return login_page_response(
            request,
            LoginPageContext(username=username or "", errors=result.errors),
        )

    token = encode_user_login_info(result.login_info)  # type: ignore

    response = RedirectResponse(url="/db", status_code=302)
    response.set_cookie(key="id_token", value=token)

    return response


@router.get("/logout")
async def logout():
    response = RedirectResponse(url="/db/login", status_code=302)
    response.delete_cookie(key="id_token")

    return response


@router.get("/tables")
async def list_tables(request: Request, user: Guest):
    if not user:
        return anonymous_user_redirect()

    if not user.is_authorized:
        raise HTTPException(status_code=401)

    tables = get_all_tables()
    return tables_view_response(request, TablesViewContext(tables=tables))


@router.get("/tables/private/{table_id}/rows")
async def private_table_rows(request: Request, table_id: int, user: Owner):
    if not user:
        return anonymous_user_redirect()

    if not user.is_authorized:
        raise HTTPException(status_code=401)

    table = get_private_table(table_id=table_id)

    if not table:
        return not_found_error_response(request)

    attributes = get_table_attributes(table_id=table_id)
    rows = get_table_rows(table_title=table.title)

    return table_rows_response(
        request, TableRowsContext(table=table, attributes=attributes, rows=rows)
    )


@router.get("/tables/{table_id}/rows")
async def public_table_rows(request: Request, table_id: int, user: Guest):
    if not user:
        return anonymous_user_redirect()

    if not user.is_authorized:
        raise HTTPException(status_code=401)

    table = get_public_table(table_id=table_id)

    if not table:
        return not_found_error_response(request)

    attributes = get_table_attributes(table_id=table_id)
    rows = get_table_rows(table_title=table.title)

    return table_rows_response(
        request, TableRowsContext(table=table, attributes=attributes, rows=rows)
    )


@router.get("/tables/{table_id}/attributes")
async def table_attributes(request: Request, table_id: int, user: Guest):
    if not user:
        return anonymous_user_redirect()

    if not user.is_authorized:
        raise HTTPException(status_code=401)

    table = get_table(table_id=table_id)

    if not table:
        return not_found_error_response(request)

    columns = get_attribute_columns()
    rows = get_table_attributes(table_id=table_id)

    print(columns)
    print(rows)

    return table_attributes_response(
        request, TableAttributesContext(table=table, columns=columns, rows=rows)
    )


@router.get("/tables/new")
async def table_create_page(request: Request, user: Owner):
    if not user:
        return anonymous_user_redirect()

    if not user.is_authorized:
        raise HTTPException(status_code=401)

    return table_create_response(request, TableCreateContext())


@router.post("/tables/new")
async def handle_table_create(
    request: Request,
    user: Owner,
    title: Annotated[str, Form()],
    is_private: Annotated[bool, Form()] = False,
    is_protected: Annotated[bool, Form()] = False,
):
    if not user:
        return anonymous_user_redirect()

    if not user.is_authorized:
        raise HTTPException(status_code=401)

    dto = CreateTableDto.defer(
        title=title, is_private=is_private, is_protected=is_protected
    )

    result = create_table(dto)

    if result.errors:
        return table_create_response(
            request,
            TableCreateContext(
                title=title,
                is_private=is_private,
                is_protected=is_protected,
                errors=result.errors,
            ),
        )

    return RedirectResponse(url=f"/db/tables/{result.table_id}/rows", status_code=302)

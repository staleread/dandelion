from typing import Annotated
from fastapi import APIRouter, Request, Form, HTTPException, Depends
from fastapi.responses import RedirectResponse

from app.common.utils.sql_runner import SqlRunner
from app.common.dependencies import ConnectionDep, SqlRunnerDep
from ..domain.dtos import LoginDto, CreateTableDto, AttributeCreateDto
from ..domain.service import login_user, create_table, create_attribute
from ..data.models import Table, Attribute, Permission, AttributeRich, DataType
from .utils.jwt import encode_user_login_info
from .dependencies import GuestDep, get_guest_user, get_owner_user, get_admin_user
from .page_contexts import (
    LoginPageContext,
    HomePageContext,
    TablesViewContext,
    TableRowsContext,
    TableAttributesContext,
    TableCreateContext,
    AttributeCreateContext,
)
from .responses import (
    login_page_response,
    home_page_response,
    tables_view_response,
    table_rows_response,
    table_attributes_response,
    table_create_response,
    attribute_create_response,
)

router = APIRouter(prefix="/db")


@router.get("/")
async def home_page(request: Request, user: GuestDep):
    return home_page_response(request, HomePageContext(username=user.username))


@router.get("/login")
async def login_page(request: Request):
    return login_page_response(request, LoginPageContext())


@router.post("/login")
async def handle_login(
    request: Request,
    username: Annotated[str | None, Form()],
    password: Annotated[str | None, Form()],
    connection: ConnectionDep,
):
    dto = LoginDto.defer(username=username, password=password)
    result = login_user(dto, connection=connection)

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


@router.get("/tables", dependencies=[Depends(get_guest_user())])
async def list_tables(request: Request, sql: SqlRunnerDep):
    tables = sql.query("""
        select * from metadata.table
    """).all(Table)

    return tables_view_response(request, TablesViewContext(tables=tables))


@router.get("/tables/{table_id}/rows")
async def public_table_rows(
    request: Request, table_id: int, user: GuestDep, sql: SqlRunnerDep
):
    table = (
        sql.query("""
        select * from metadata.table
        where id = :table_id
    """)
        .bind(table_id=table_id)
        .first(Table)
    )

    if not table:
        raise HTTPException(status_code=404)

    if table.is_private and Permission.CAN_READ_PRIVATE not in user.permissions:
        raise HTTPException(status_code=403)

    attributes = (
        sql.query("""
        select 
            a.id,
            a.table_id,
            a.name,
            a.ukr_name,
            dt.name as data_type,
            a.is_primary,
            a.is_unique,
            a.is_nullable,
            (fk.attribute_id is not null) as is_foreign
        from metadata.attribute a
        left join metadata.foreign_key fk on fk.attribute_id = a.id
        join metadata.data_type dt on dt.id = a.data_type_id
        where a.table_id = :table_id
    """)
        .bind(table_id=table_id)
        .all(Attribute)
    )

    rows = sql.query(f"""
        select * from "{table.title}"
    """).many()

    return table_rows_response(
        request, TableRowsContext(table=table, attributes=attributes, rows=rows)
    )


@router.get("/tables/{table_id}/attributes", dependencies=[Depends(get_guest_user())])
async def table_attributes(request: Request, table_id: int, sql: SqlRunnerDep):
    table = (
        sql.query("""
        select * from metadata.table
        where id = :table_id
    """)
        .bind(table_id=table_id)
        .first(Table)
    )

    if not table:
        raise HTTPException(status_code=404)

    rows = (
        sql.query("""
        select 
            a.id,
            a.table_id,
            a.name,
            a.ukr_name,
            dt.name as data_type,
            a.is_primary,
            a.is_unique,
            a.is_nullable,
            ft.id as foreign_table_id,
            ft.title as foreign_table_name
        from metadata.attribute a
        join metadata.data_type dt on dt.id = a.data_type_id
        left join metadata.foreign_key fk on fk.attribute_id = a.id
        left join metadata.attribute ra on ra.id = fk.referenced_attribute_id
        left join metadata.table ft on ft.id = ra.table_id
        where a.table_id = :table_id
    """)
        .bind(table_id=table_id)
        .all(AttributeRich)
    )

    return table_attributes_response(
        request, TableAttributesContext(table=table, rows=rows)
    )


@router.get("/tables/new", dependencies=[Depends(get_owner_user())])
async def table_create_page(request: Request):
    return table_create_response(request, TableCreateContext())


@router.post("/tables/new", dependencies=[Depends(get_owner_user())])
async def handle_table_create(
    request: Request,
    title: Annotated[str, Form()],
    connection: ConnectionDep,
    is_private: Annotated[bool, Form()] = False,
    is_protected: Annotated[bool, Form()] = False,
):
    dto = CreateTableDto.defer(
        title=title, is_private=is_private, is_protected=is_protected
    )

    result = create_table(dto, connection=connection)

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

    return RedirectResponse(
        url=f"/db/tables/{result.table_id}/attributes", status_code=302
    )


@router.get(
    "/tables/{table_id}/attributes/new", dependencies=[Depends(get_admin_user())]
)
async def attribute_create_page(request: Request, table_id: int, sql: SqlRunnerDep):
    table = (
        sql.query("""
        select * from metadata.table
        where id = :table_id
        """)
        .bind(table_id=table_id)
        .first(Table)
    )

    if not table:
        raise HTTPException(status_code=404)

    data_types = sql.query("""
        select * from metadata.data_type
    """).all(DataType)

    return attribute_create_response(
        request, AttributeCreateContext(table=table, data_types=data_types)
    )


@router.post(
    "/tables/{table_id}/attributes/new", dependencies=[Depends(get_admin_user())]
)
async def handle_attribute_create(
    request: Request,
    table_id: int,
    name: Annotated[str, Form()],
    ukr_name: Annotated[str, Form()],
    data_type_id: Annotated[int, Form()],
    connection: ConnectionDep,
    is_unique: Annotated[bool, Form()] = False,
    is_nullable: Annotated[bool, Form()] = False,
):
    dto = AttributeCreateDto.defer(
        table_id=table_id,
        name=name,
        ukr_name=ukr_name,
        data_type_id=data_type_id,
        is_unique=is_unique,
        is_nullable=is_nullable,
    )

    result = create_attribute(dto, connection=connection)

    if not result.errors:
        return RedirectResponse(
            url=f"/db/tables/{table_id}/attributes", status_code=302
        )

    sql = SqlRunner(connection=connection)

    table = (
        sql.query("""
        select * from metadata.table
        where id = :table_id
    """)
        .bind(table_id=table_id)
        .first(Table)
    )

    data_types = sql.query("""
        select * from metadata.data_type
    """).all(DataType)

    return attribute_create_response(
        request,
        AttributeCreateContext(
            table=table,
            data_types=data_types,
            name=name,
            ukr_name=ukr_name,
            data_type_id=data_type_id,
            is_unique=is_unique,
            is_nullable=is_nullable,
            errors=result.errors,
        ),
    )

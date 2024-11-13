from typing import Annotated
from fastapi import APIRouter, Depends, Form, HTTPException
from fastapi.responses import RedirectResponse

from app.common.database.utils import QueryRunnerDep, ConnectionDep
from app.common.template.utils import TemplateModelDep
from app.common.exceptions import ValidationException

from ..auth.enums import Permissions
from ..auth.utils import get_guest_user, get_admin_user, get_owner_user, GuestDep
from ..table_row.service import get_table_rows
from ..table_attribute.service import (
    get_table_attributes,
    get_table_rich_attributes,
    get_all_data_types,
)
from .models import (
    Table,
    TablesView,
    TableCreate,
    TableCreateResponse,
    TableAttributesView,
    AttributeSecondaryCreate,
    AttributeSecondaryCreateResponse,
    TableRowsView,
)
from .service import create_table, find_table_by_id, create_secondary_table_attribute


router = APIRouter(prefix="/table")


@router.get("/", dependencies=[Depends(get_guest_user())])
async def get_tables(sql: QueryRunnerDep, template: TemplateModelDep):
    tables = sql.query("""
        select * from metadata.table
    """).all(Table)

    return template("dba/table/tables.html", TablesView(tables=tables))


@router.get("/new", dependencies=[Depends(get_owner_user())])
async def get_new_table_form(template: TemplateModelDep):
    return template("dba/table/table_new.html", TableCreateResponse())


@router.post("/new", dependencies=[Depends(get_owner_user())])
async def post_new_table_form(
    table_create: Annotated[TableCreate, Form()],
    connection: ConnectionDep,
    template: TemplateModelDep,
):
    try:
        create_table(connection=connection, table_create=table_create)
        return RedirectResponse(url="/dba/table", status_code=302)
    except ValidationException as e:
        failure_response = TableCreateResponse(
            **table_create.model_dump(),
            errors={e.source: e.message},
        )
        return template("dba/table/table_new.html", failure_response)


@router.get("/{table_id}/attribute", dependencies=[Depends(get_guest_user())])
async def get_table_attributes_view(
    table_id: int, connection: ConnectionDep, template: TemplateModelDep
):
    table = find_table_by_id(connection=connection, table_id=table_id)

    if not table:
        raise HTTPException(status_code=404)

    rich_attributes = get_table_rich_attributes(
        connection=connection, table_id=table_id
    )

    print(rich_attributes)

    return template(
        "dba/table/table_attributes.html",
        TableAttributesView(table=table, rich_attributes=rich_attributes),
    )


@router.get("/{table_id}/attribute/new", dependencies=[Depends(get_admin_user())])
async def get_attribute_secondary_create_form(
    table_id: int, connection: ConnectionDep, template: TemplateModelDep
):
    table = find_table_by_id(connection=connection, table_id=table_id)

    if not table:
        raise HTTPException(status_code=404)

    data_types = get_all_data_types(connection=connection)

    response = AttributeSecondaryCreateResponse(
        table=table,
        data_types=data_types,
    )

    return template("dba/table/table_attribute_new.html", response)


@router.post("/{table_id}/attribute/new", dependencies=[Depends(get_admin_user())])
async def post_attribute_secondary_create_form(
    table_id: int,
    attribute_create: Annotated[AttributeSecondaryCreate, Form()],
    connection: ConnectionDep,
    template: TemplateModelDep,
):
    try:
        create_secondary_table_attribute(
            connection=connection,
            attribute_create=attribute_create,
        )

        return RedirectResponse(url=f"/dba/table/{table_id}/attribute", status_code=302)
    except ValidationException as e:
        table = find_table_by_id(connection=connection, table_id=table_id)

        if not table:
            raise HTTPException(status_code=404)

        data_types = get_all_data_types(connection=connection)

        failure_response = AttributeSecondaryCreateResponse(
            **attribute_create.model_dump(),
            table=table,
            data_types=data_types,
            errors={e.source: e.message},
        )

        return template("dba/table/table_attribute_new.html", failure_response)


@router.get("/{table_id}/row")
async def get_table_rows_view(
    table_id: int, user: GuestDep, template: TemplateModelDep, connection: ConnectionDep
):
    table = find_table_by_id(connection=connection, table_id=table_id)

    if not table:
        raise HTTPException(status_code=404)

    if table.is_private and Permissions.CAN_READ_PRIVATE not in user.permissions:
        raise HTTPException(status_code=403)

    attributes = get_table_attributes(connection=connection, table_id=table_id)

    rows = get_table_rows(connection=connection, table_title=table.title)

    return template(
        "dba/table/table_rows.html",
        TableRowsView(table=table, attributes=attributes, rows=rows),
    )

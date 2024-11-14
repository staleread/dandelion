from typing import Annotated
from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import RedirectResponse

from app.common.database.utils import QueryRunnerDep, ConnectionDep, SqlRunner
from app.common.template.utils import TemplateModelDep

from ..auth.enums import Permissions
from ..auth.utils import (
    get_guest_user,
    get_admin_user,
    get_owner_user,
    get_operator_user,
    GuestDep,
)
from ..table_attribute.service import (
    get_display_attributes,
    get_rich_display_attributes,
    get_all_data_types,
    find_attribute_by_id,
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
    RowCreateResponse,
    RowUpdateResponse,
    AttributeSecondaryEdit,
    AttributeSecondaryEditResponse,
)
from .service import (
    create_table,
    find_table_by_id,
    create_secondary_table_attribute,
    delete_table,
    get_formatted_table_rows,
    add_row,
    update_row,
    edit_secondary_table_attribute,
    delete_table_attribute,
)


router = APIRouter(prefix="/table")


@router.get("/", dependencies=[Depends(get_guest_user())])
async def get_tables(sql: QueryRunnerDep, template: TemplateModelDep):
    tables = sql.query("""
        select * from metadata.table
    """).many(lambda x: Table(**x))

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
    except ValueError as e:
        failure_response = TableCreateResponse(
            **table_create.model_dump(),
            error=str(e),
        )
        return template("dba/table/table_new.html", failure_response)


@router.post("/{table_id}/delete", dependencies=[Depends(get_owner_user())])
async def delete_table_handler(
    table_id: int,
    connection: ConnectionDep,
):
    try:
        delete_table(connection=connection, table_id=table_id)
        return RedirectResponse(url="/dba/table", status_code=302)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{table_id}/attribute", dependencies=[Depends(get_guest_user())])
async def get_table_attributes_view(
    table_id: int, connection: ConnectionDep, template: TemplateModelDep
):
    table = find_table_by_id(connection=connection, table_id=table_id)

    if not table:
        raise HTTPException(status_code=404)

    rich_attributes = get_rich_display_attributes(
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
    except ValueError as e:
        table = find_table_by_id(connection=connection, table_id=table_id)

        if not table:
            raise HTTPException(status_code=404)

        data_types = get_all_data_types(connection=connection)

        failure_response = AttributeSecondaryCreateResponse(
            **attribute_create.model_dump(),
            table=table,
            data_types=data_types,
            error=str(e),
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

    attributes = get_display_attributes(connection=connection, table_id=table_id)

    rows = get_formatted_table_rows(
        connection=connection, table_title=table.title, attributes=attributes
    )

    return template(
        "dba/table/table_rows.html",
        TableRowsView(table=table, attributes=attributes, rows=rows),
    )


@router.get("/{table_id}/row/new", dependencies=[Depends(get_admin_user())])
async def get_row_create_form(
    table_id: int,
    connection: ConnectionDep,
    template: TemplateModelDep,
):
    table = find_table_by_id(connection=connection, table_id=table_id)
    if not table:
        raise HTTPException(status_code=404)

    attributes = [
        attr
        for attr in get_display_attributes(connection=connection, table_id=table_id)
        if attr.data_type != "serial"
    ]

    view = RowCreateResponse(table=table, attributes=attributes)

    return template("dba/table/table_row_new.html", view)


@router.post("/{table_id}/row/new", dependencies=[Depends(get_operator_user())])
async def post_row_create_form(
    table_id: int,
    request: Request,
    connection: ConnectionDep,
    template: TemplateModelDep,
):
    table = find_table_by_id(connection=connection, table_id=table_id)

    if not table:
        raise HTTPException(status_code=404)

    form_data = await request.form()
    row_data = dict(form_data)

    try:
        add_row(
            connection=connection,
            table_id=table_id,
            values=row_data,
        )
        return RedirectResponse(url=f"/dba/table/{table_id}/row", status_code=302)
    except ValueError as e:
        attributes = [
            attr
            for attr in get_display_attributes(connection=connection, table_id=table_id)
            if attr.data_type != "serial"
        ]

        return template(
            "dba/table/table_row_new.html",
            RowCreateResponse(
                table=table,
                attributes=attributes,
                values=row_data,
                error=str(e),
            ),
        )


@router.get("/{table_id}/row/{row_id}/edit", dependencies=[Depends(get_admin_user())])
async def get_row_update_form(
    table_id: int,
    row_id: int,
    connection: ConnectionDep,
    template: TemplateModelDep,
):
    table = find_table_by_id(connection=connection, table_id=table_id)
    if not table:
        raise HTTPException(status_code=404)

    row = (
        SqlRunner(connection=connection)
        .query(f'select * from "{table.title}" where id = :row_id')
        .bind(row_id=row_id)
        .first_row()
    )

    if not row:
        raise HTTPException(status_code=404)

    attributes = [
        attr
        for attr in get_display_attributes(connection=connection, table_id=table_id)
        if attr.data_type != "serial"
    ]

    return template(
        "dba/table/table_row_edit.html",
        RowUpdateResponse(
            table=table, attributes=attributes, row_id=row_id, values=row
        ),
    )


@router.post(
    "/{table_id}/row/{row_id}/edit", dependencies=[Depends(get_operator_user())]
)
async def post_row_update_form(
    table_id: int,
    row_id: int,
    request: Request,
    connection: ConnectionDep,
    template: TemplateModelDep,
):
    table = find_table_by_id(connection=connection, table_id=table_id)
    if not table:
        raise HTTPException(status_code=404)

    attributes = [
        attr
        for attr in get_display_attributes(connection=connection, table_id=table_id)
        if attr.data_type != "serial"
    ]

    form_data = await request.form()
    row_data = dict(form_data)

    try:
        update_row(
            connection=connection, table_id=table_id, row_id=row_id, values=row_data
        )
        return RedirectResponse(url=f"/dba/table/{table_id}/row", status_code=302)
    except ValueError as e:
        return template(
            "dba/table/table_row_edit.html",
            RowUpdateResponse(
                table=table,
                attributes=attributes,
                row_id=row_id,
                values=row_data,
                error=str(e),
            ),
        )


@router.get(
    "/{table_id}/attribute/{attribute_id}/edit",
    dependencies=[Depends(get_admin_user())],
)
async def get_attribute_edit_form(
    table_id: int,
    attribute_id: int,
    connection: ConnectionDep,
    template: TemplateModelDep,
):
    table = find_table_by_id(connection=connection, table_id=table_id)
    if not table:
        raise HTTPException(status_code=404)

    attribute = find_attribute_by_id(
        connection=connection, table_id=table_id, attribute_id=attribute_id
    )

    if not attribute:
        raise HTTPException(status_code=404)

    if attribute.is_primary:
        raise HTTPException(
            status_code=403, detail="Не можна редагувати первинний ключ"
        )

    return template(
        "dba/table/table_attribute_edit.html",
        AttributeSecondaryEditResponse(
            table=table,
            attribute=attribute,
            name=attribute.name,
            ukr_name=attribute.ukr_name,
        ),
    )


@router.post(
    "/{table_id}/attribute/{attribute_id}/edit",
    dependencies=[Depends(get_admin_user())],
)
async def post_attribute_edit_form(
    table_id: int,
    attribute_id: int,
    attribute_edit: Annotated[AttributeSecondaryEdit, Form()],
    connection: ConnectionDep,
    template: TemplateModelDep,
):
    try:
        edit_secondary_table_attribute(
            connection=connection,
            table_id=table_id,
            attribute_id=attribute_id,
            name=attribute_edit.name,
            ukr_name=attribute_edit.ukr_name,
        )
        return RedirectResponse(url=f"/dba/table/{table_id}/attribute", status_code=302)
    except ValueError as e:
        table = find_table_by_id(connection=connection, table_id=table_id)

        attribute = find_attribute_by_id(
            connection=connection, table_id=table_id, attribute_id=attribute_id
        )

        if not table or not attribute:
            raise HTTPException(status_code=404)

        return template(
            "dba/table/table_attribute_edit.html",
            AttributeSecondaryEditResponse(
                table=table,
                attribute=attribute,
                name=attribute_edit.name,
                ukr_name=attribute_edit.ukr_name,
                error=str(e),
            ),
        )


@router.post(
    "/{table_id}/attribute/{attribute_id}/delete",
    dependencies=[Depends(get_admin_user())],
)
async def delete_attribute_handler(
    table_id: int,
    attribute_id: int,
    connection: ConnectionDep,
):
    try:
        delete_table_attribute(
            connection=connection,
            table_id=table_id,
            attribute_id=attribute_id,
        )
        return RedirectResponse(url=f"/dba/table/{table_id}/attribute", status_code=302)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

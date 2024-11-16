from fastapi import APIRouter, Request, Response

from app.common.database.utils import QueryRunnerDep, ConnectionDep
from app.common.template.utils import TemplateContextDep
from .service import create_document, get_document_template

router = APIRouter(prefix="/command")


@router.get("/document")
def get_documents_view(sql: QueryRunnerDep, template: TemplateContextDep):
    documents = sql.query("""
        SELECT id, name FROM document_type
    """).many_rows()

    return template("/classic/command/documents.html", {"documents": documents})


@router.get("/document/{document_id}")
def get_document_create_form(
    document_id: int, connection: ConnectionDep, template: TemplateContextDep
):
    document_template = get_document_template(
        connection=connection, document_type_id=document_id
    )

    return template(
        "/classic/command/document_new.html",
        {"document_id": document_id, "document_fields": document_template},
    )


@router.post("/document/{document_id}/create")
async def post_document_create_form(
    request: Request,
    document_id: int,
    connection: ConnectionDep,
    template: TemplateContextDep,
):
    try:
        form_data = dict(await request.form())

        visit_id = int(str(form_data["visit_id"]))
        issue_date = str(form_data["issue_date"])

        document_data = {
            k: v for k, v in form_data.items() if k not in ["visit_id", "issue_date"]
        }

        pdf_bytes = create_document(
            connection=connection,
            document_id=document_id,
            visit_id=visit_id,
            issue_date=issue_date,
            document_data=document_data,
        )

        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename=document_{document_id}_{issue_date}.pdf"
            },
        )

    except ValueError as e:
        document_template = get_document_template(
            connection=connection, document_type_id=document_id
        )

        return template(
            "/classic/command/document_new.html",
            {
                "document_id": document_id,
                "document_fields": document_template,
                "error": str(e),
            },
        )

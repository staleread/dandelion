from sqlalchemy.engine import Connection
from datetime import datetime
import json

from app.common.database.utils import SqlRunner
from app.common.template.core import pdf_templates
import pdfkit  # type: ignore


def create_document(
    *,
    connection: Connection,
    document_id: int,
    visit_id: int,
    issue_date: str,
    document_data: dict,
) -> bytes:
    issue_date_obj = datetime.strptime(issue_date, "%Y-%m-%d")

    if issue_date_obj > datetime.now():
        raise ValueError("Дата видачі не може бути в майбутньому")

    if "issue_date" in document_data:
        document_data["issue_date"] = issue_date_obj.strftime("%d.%m.%Y")

    template = pdf_templates.get_template(f"docs/template_{document_id}.html")

    html_content = template.render(document_data=document_data)

    pdf_bytes = bytes(
        pdfkit.from_string(html_content, False, options={"encoding": "utf-8"})
    )

    SqlRunner(connection=connection).query("""
        INSERT INTO document (visit_id, document_type_id, data)
        VALUES (:visit_id, :document_type_id, :data)
    """).bind(
        visit_id=visit_id, document_type_id=document_id, data=json.dumps(document_data)
    ).execute()

    return pdf_bytes


def get_document_template(*, connection: Connection, document_type_id: int) -> dict:
    return (
        SqlRunner(connection=connection)
        .query("""
        SELECT template FROM document_type WHERE id = :document_type_id
    """)
        .bind(document_type_id=document_type_id)
        .scalar()
    )

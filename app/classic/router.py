from fastapi import APIRouter, Request
from app.core.templating import templates

router = APIRouter()


@router.get("/")
async def get_tables_page(request: Request):
    context = {
        "user": {
            "username": "Nicolas",
        }
    }
    return templates.TemplateResponse(
        request=request, name="classic/home.html", context=context
    )

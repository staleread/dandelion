from fastapi import APIRouter, Request
from app.core.templating import TemplateResponse

router = APIRouter()


@router.get("/")
async def get_tables_page(request: Request):
    context = {
        "user": {
            "username": "Nicolas",
        }
    }
    return TemplateResponse(request=request, name="classic/home.html", context=context)

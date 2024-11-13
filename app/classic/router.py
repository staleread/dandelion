from fastapi import APIRouter

from app.common.template.utils import TemplateContextDep


router = APIRouter(prefix="/classic")


@router.get("/")
async def get_home_page(template: TemplateContextDep):
    return template("/classic/home.html", {})

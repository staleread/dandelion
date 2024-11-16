from fastapi import APIRouter

from app.common.template.utils import TemplateContextDep
from app.classic.query.views import router as query_router
from app.classic.command.views import router as command_router

router = APIRouter(prefix="/classic")


@router.get("/")
async def get_home_page(template: TemplateContextDep):
    return template("/classic/home.html", {})


router.include_router(query_router)
router.include_router(command_router)

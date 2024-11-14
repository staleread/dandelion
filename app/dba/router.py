from fastapi import APIRouter
from pydantic import BaseModel
from app.common.template.utils import TemplateModelDep

from .user.utils import GuestDep
from .user.views import router as user_router
from .table.views import router as table_router


router = APIRouter(prefix="/dba")


class DbaHomeView(BaseModel):
    username: str


@router.get("/")
async def get_home_page(template: TemplateModelDep, user: GuestDep):
    return template("dba/home.html", DbaHomeView(username=user.username))


router.include_router(user_router)
router.include_router(table_router)

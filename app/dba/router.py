from fastapi import APIRouter
from pydantic import BaseModel
from app.common.template.utils import TemplateModelDep

from .auth.utils import GuestDep
from .auth.views import router as auth_router
from .table.views import router as table_router


router = APIRouter(prefix="/dba")


class DbaHomeView(BaseModel):
    username: str


@router.get("/")
async def get_home_page(template: TemplateModelDep, user: GuestDep):
    return template("dba/home.html", DbaHomeView(username=user.username))


router.include_router(auth_router)
router.include_router(table_router)

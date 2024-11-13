from typing import Annotated
from fastapi import APIRouter, Form
from fastapi.responses import RedirectResponse

from app.config import settings
from app.common.template.utils import TemplateModelDep
from app.common.database.utils import ConnectionDep

from .service import login_user
from .models import UserLogin, UserLoginResponse


router = APIRouter(prefix="/auth")


@router.get("/login")
async def get_login_form(template: TemplateModelDep):
    return template("dba/auth/login.html", UserLoginResponse())


@router.post("/login")
async def post_login_form(
    user_login: Annotated[UserLogin, Form()],
    template: TemplateModelDep,
    connection: ConnectionDep,
):
    try:
        token = login_user(connection=connection, user_login=user_login)

        response = RedirectResponse(url="/dba", status_code=302)
        response.set_cookie(key=settings.cookie_name, value=token)

        return response
    except ValueError as e:
        failure_response = UserLoginResponse(
            **user_login.model_dump(),
            error=str(e),
        )
        return template("dba/auth/login.html", failure_response)


@router.get("/logout")
async def get_logout():
    response = RedirectResponse(url="/dba/auth/login", status_code=302)
    response.delete_cookie(key=settings.cookie_name)

    return response

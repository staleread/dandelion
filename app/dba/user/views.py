from typing import Annotated
from fastapi import APIRouter, Form, Depends
from fastapi.responses import RedirectResponse

from app.config import settings
from app.common.template.utils import TemplateModelDep, TemplateContextDep
from app.common.database.utils import ConnectionDep, QueryRunnerDep
from app.dba.user.utils import GuestDep, get_guest_user

from .service import login_user, get_available_roles, add_user, reset_password
from .models import (
    UserLogin,
    UserLoginResponse,
    UserAdd,
    UserAddResponse,
    DisplayUser,
    UserReset,
    UserResetResponse,
)


router = APIRouter(prefix="/user")


@router.get("/", dependencies=[Depends(get_guest_user())])
async def get_users_view(template: TemplateContextDep, sql: QueryRunnerDep):
    display_users = sql.query("""
        select u.id, u.username, r.name as role
        from "user" u
        join "role" r on u.role_id = r.id
    """).many(lambda x: DisplayUser(**x))

    return template("dba/user/users.html", {"users": display_users})


@router.get("/login")
async def get_login_form(template: TemplateModelDep):
    return template("dba/user/login.html", UserLoginResponse())


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
        return template("dba/user/login.html", failure_response)


@router.get("/logout")
async def get_logout():
    response = RedirectResponse(url="/dba/user/login", status_code=302)
    response.delete_cookie(key=settings.cookie_name)

    return response


@router.get("/add", dependencies=[Depends(get_guest_user())])
async def get_user_add_form(template: TemplateModelDep, connection: ConnectionDep):
    available_roles = get_available_roles(connection=connection)
    return template(
        "dba/user/user_add.html", UserAddResponse(available_roles=available_roles)
    )


@router.post("/add")
async def post_user_add_form(
    user_add: Annotated[UserAdd, Form()],
    template: TemplateModelDep,
    connection: ConnectionDep,
    user_info: GuestDep,
):
    try:
        add_user(
            connection=connection,
            user_add=user_add,
            current_user_permissions=user_info.permissions,
        )
        return RedirectResponse(url="/dba/user", status_code=302)
    except ValueError as e:
        available_roles = get_available_roles(connection=connection)
        failure_response = UserAddResponse(
            **user_add.model_dump(), error=str(e), available_roles=available_roles
        )
        return template("dba/user/user_add.html", failure_response)


@router.get("/reset")
async def get_reset_form(template: TemplateModelDep):
    return template("dba/user/reset.html", UserResetResponse())


@router.post("/reset")
async def post_reset_form(
    user_reset: Annotated[UserReset, Form()],
    template: TemplateModelDep,
    connection: ConnectionDep,
):
    try:
        reset_password(connection=connection, user_reset=user_reset)
        return RedirectResponse(url="/dba/user/login", status_code=302)
    except ValueError as e:
        failure_response = UserResetResponse(**user_reset.model_dump(), error=str(e))
        return template("dba/user/reset.html", failure_response)

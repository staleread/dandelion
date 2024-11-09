from typing import Annotated
from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from pydantic import ValidationError

from app.common.exceptions import NotFoundException, PasswordsDontMatchException
from app.core.templating import TemplateResponse
from .service import get_login_token
from .repo import repo
from .dto import LoginDto
from .auth import Guest, Owner
from .utils import extract_error_messages, get_rows_from_table

router = APIRouter(prefix="/db")

AnonymousUserRedirect = RedirectResponse(url="/db/login", status_code=302)


@router.get("/")
async def home_page(request: Request, user: Guest):
    if not user:
        return AnonymousUserRedirect

    if not user.is_authorized:
        return TemplateResponse(
            request=request,
            name="dba/errors/unauthorized.html",
        )

    return TemplateResponse(
        request=request,
        name="dba/home.html",
        context={"username": user.username},
    )


@router.get("/login")
async def login_form(request: Request, user: Guest):
    if user and user.is_authorized:
        return RedirectResponse(url="/db", status_code=302)

    return TemplateResponse(request=request, name="dba/login.html")


@router.post("/login")
async def handle_login_user(
    request: Request,
    username: Annotated[str | None, Form()],
    password: Annotated[str | None, Form()],
):
    def back_to_login_response(errors: dict):
        return TemplateResponse(
            request=request,
            name="dba/login.html",
            context={"username": username} | errors,
        )

    try:
        dto = LoginDto.defer(username=username, password=password)
        token = get_login_token(dto)

        response = RedirectResponse(url="/db", status_code=302)
        response.set_cookie(key="id_token", value=token)

        return response
    except ValidationError as e:
        return back_to_login_response(extract_error_messages(e))
    except NotFoundException:
        return back_to_login_response(
            {
                "username_error": "Користувача не знайдено",
            }
        )
    except PasswordsDontMatchException:
        return back_to_login_response(
            {
                "password_error": "Неправильний пароль",
            }
        )
    except Exception:
        return TemplateResponse(
            request=request,
            name="dba/errors/internal.html",
        )


@router.get("/logout")
async def logout():
    response = RedirectResponse(url="/db/login", status_code=302)
    response.delete_cookie(key="id_token")

    return response


@router.get("/tables")
async def list_tables(request: Request, user: Guest):
    if not user:
        return AnonymousUserRedirect

    if not user.is_authorized:
        return TemplateResponse(
            request=request,
            name="dba/errors/unauthorized.html",
        )

    tables = repo.all_table_names()

    return TemplateResponse(
        request=request, name="dba/tables.html", context={"tables": tables}
    )


@router.get("/tables/user/view")
async def view_users(request: Request, user: Owner):
    return await view_table(request, "user", user)


@router.get("/tables/{table_name}/view")
async def view_table(request: Request, table_name: str, user: Guest):
    if not user:
        return AnonymousUserRedirect

    if not user.is_authorized:
        return TemplateResponse(
            request=request,
            name="dba/errors/unauthorized.html",
        )

    try:
        columns = list(repo.table_columns(table_name=table_name))
        rows = get_rows_from_table(table_name)

        return TemplateResponse(
            request=request,
            name="dba/table_view.html",
            context={
                "table_name": table_name,
                "columns": columns,
                "rows": rows,
            },
        )
    except Exception:
        return TemplateResponse(
            request=request,
            name="dba/errors/internal.html",
        )

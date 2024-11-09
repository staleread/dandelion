from typing import Annotated
from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from pydantic import ValidationError

from app.common.exceptions import NotFoundException, PasswordsDontMatchException
from app.core.templating import TemplateResponse
from .service import get_login_info
from .repo import repo
from .dto import LoginDto
from .auth import Guest
from .utils import extract_error_messages

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
        login_info, token = get_login_info(dto)

        response = TemplateResponse(
            request=request,
            name="dba/home.html",
            context={"username": login_info.username},
        )
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
async def list_tables(request: Request):
    tables = list(map(lambda t: t["table_name"], repo.all_table_names()))

    return TemplateResponse(
        request=request, name="dba/tables.html", context={"tables": tables}
    )


@router.get("/tables/{table_name}")
async def view_table(request: Request, table_name: str):
    try:
        columns = repo.table_columns(table_name)
        rows = repo.table_rows(table_name)

        return TemplateResponse(
            request=request,
            name="dba/table_view.html",
            context={"table_name": table_name, "columns": columns, "rows": rows},
        )
    except Exception:
        return TemplateResponse(
            request=request,
            name="dba/errors/internal.html",
        )

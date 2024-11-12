import traceback
from fastapi import FastAPI, Request
from app.core.api import api_router
from app.common.responses import (
    internal_error_response,
    not_found_error_response,
    forbidden_error_response,
)
from app.dba.views.responses import unauthorized_user_redirect

app = FastAPI()


@app.exception_handler(401)
async def unauthorized_exception_handler(request: Request, _):
    return unauthorized_user_redirect()


@app.exception_handler(403)
async def forbidden_exception_handler(request: Request, _):
    return forbidden_error_response(request)


@app.exception_handler(404)
async def not_found_exception_handler(request: Request, _):
    return not_found_error_response(request)


@app.exception_handler(500)
async def internal_error_exception_handler(request: Request, _):
    print(traceback.format_exc())
    return internal_error_response(request)


app.include_router(api_router)

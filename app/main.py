import traceback
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse

from app.common.template.core import templates
from app.classic.router import router as classic_router
from app.dba.router import router as dba_router


app = FastAPI()


@app.exception_handler(401)
async def unauthorized_exception_handler(_, __):
    return RedirectResponse(url="/dba/auth/login")


@app.exception_handler(403)
async def forbidden_exception_handler(request: Request, _):
    return templates.TemplateResponse(request, name="errors/403.html")


@app.exception_handler(404)
async def not_found_exception_handler(request: Request, _):
    return templates.TemplateResponse(request, name="errors/404.html")


@app.exception_handler(500)
async def internal_error_exception_handler(request: Request, _):
    print(traceback.format_exc())
    return templates.TemplateResponse(request, name="errors/500.html")


@app.get("/")
async def redirect_to_classic():
    return RedirectResponse(url="/classic")


app.include_router(classic_router)
app.include_router(dba_router)

from fastapi import APIRouter

from app.classic.router import router as classic_router
from app.dba.views.routes import router as dba_router

api_router = APIRouter()

api_router.include_router(classic_router)
api_router.include_router(dba_router)

from typing import Annotated, Callable
from fastapi import Depends, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from .core import templates


def get_template_model_response(
    request: Request,
) -> Callable[[str, BaseModel], HTMLResponse]:
    def template_model_response(name: str, model: BaseModel) -> HTMLResponse:
        return templates.TemplateResponse(
            request, name=name, context=model.model_dump()
        )

    return template_model_response


TemplateModelDep = Annotated[
    Callable[[str, BaseModel], HTMLResponse],
    Depends(get_template_model_response),
]


def get_template_response(request: Request) -> Callable[[str, dict], HTMLResponse]:
    def template_response(name: str, context: dict) -> HTMLResponse:
        return templates.TemplateResponse(request, name=name, context=context)

    return template_response


TemplateContextDep = Annotated[
    Callable[[str, dict], HTMLResponse],
    Depends(get_template_response),
]

from pydantic import BaseModel

from .models import UserLoginInfo


class LoginResult(BaseModel):
    login_info: UserLoginInfo | None = None
    errors: dict[str, str] | None = None


class TableCreateResult(BaseModel):
    table_id: int | None = None
    errors: dict[str, str] | None = None


class AttributeCreateResult(BaseModel):
    attribute_id: int | None = None
    errors: dict[str, str] | None = None

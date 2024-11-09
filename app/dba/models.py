from pydantic import BaseModel
from pydantic.dataclasses import dataclass


class UserLoginInfo(BaseModel):
    username: str
    permissions: list[str]


@dataclass
class UserInfo:
    username: str | None
    is_authorized: bool = False

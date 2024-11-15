from pydantic import BaseModel, ConfigDict

from .enums import Permissions


class User(BaseModel):
    id: int
    role_id: int
    username: str
    hashed_password: str


class DisplayUser(BaseModel):
    id: int
    role: str
    username: str


class UserLogin(BaseModel):
    username: str = ""
    password: str = ""


class UserLoginResponse(UserLogin):
    error: str = ""


class UserReset(BaseModel):
    username: str = ""
    password: str = ""


class UserResetResponse(UserReset):
    error: str = ""


class UserTokenPayload(BaseModel):
    # ignore JWT claims
    model_config = ConfigDict(extra="ignore")

    username: str
    permissions: list[Permissions]


class UserInfo(BaseModel):
    username: str
    permissions: set[Permissions]


class Role(BaseModel):
    id: int
    name: str


class UserAdd(BaseModel):
    username: str = ""
    password: str = ""
    role: int = 0


class UserAddResponse(UserAdd):
    error: str = ""
    available_roles: list[Role] = []

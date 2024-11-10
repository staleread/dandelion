from pydantic import BaseModel


class User(BaseModel):
    id: int
    role_id: int
    username: str
    hashed_password: str


class Table(BaseModel):
    id: int
    title: str
    is_private: bool
    is_protected: bool


class Attribute(BaseModel):
    id: int
    name: str
    ukr_name: str
    type: str
    is_primary: bool

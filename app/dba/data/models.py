from enum import StrEnum
from pydantic import BaseModel


class User(BaseModel):
    id: int
    role_id: int
    username: str
    hashed_password: str


class Permission(StrEnum):
    CAN_CONNECT = "can_connect"
    CAN_READ_PUBLIC = "can_read_public"
    CAN_MODIFY_RECORDS = "can_modify_records"
    CAN_MODIFY_ATTRIBUTES = "can_modify_attributes"
    CAN_ADD_USER = "can_add_user"
    CAN_ADD_OPERATOR = "can_add_operator"
    CAN_READ_PRIVATE = "can_read_private"
    CAN_MODIFY_TABLES = "can_modify_tables"
    CAN_ADD_ADMIN = "can_add_admin"


class Table(BaseModel):
    id: int
    title: str
    is_private: bool
    is_protected: bool


class AttributeBase(BaseModel):
    id: int
    table_id: int
    name: str
    ukr_name: str
    data_type: str
    is_primary: bool
    is_unique: bool
    is_nullable: bool


class Attribute(AttributeBase):
    is_foreign: bool


class AttributeRich(AttributeBase):
    foreign_table_id: int | None
    foreign_table_name: str | None


class DataType(BaseModel):
    id: int
    name: str

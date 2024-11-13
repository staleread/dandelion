from pydantic import BaseModel


class DataType(BaseModel):
    id: int
    name: str


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

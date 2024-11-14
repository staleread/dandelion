from pydantic import BaseModel


class DataType(BaseModel):
    id: int
    name: str


class Attribute(BaseModel):
    id: int
    table_id: int
    name: str
    ukr_name: str
    is_primary: bool
    is_unique: bool
    is_nullable: bool
    constraint_pattern: str | None


class DisplayAttribute(Attribute):
    data_type: str
    is_foreign: bool


class DisplayAttributeRich(Attribute):
    data_type: str
    foreign_table_id: int | None
    foreign_table_name: str | None

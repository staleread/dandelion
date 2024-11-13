from pydantic import BaseModel
from ..table_attribute.models import Attribute, AttributeRich, DataType
from typing import Any


class BaseForm(BaseModel):
    error: str | None = None


class Table(BaseModel):
    id: int
    title: str
    is_private: bool
    is_protected: bool


class TablesView(BaseModel):
    tables: list[Table]


class TableAttributesView(BaseModel):
    table: Table
    rich_attributes: list[AttributeRich]


class TableRowsView(BaseModel):
    table: Table
    attributes: list[Attribute]
    rows: list[dict]


class TableCreate(BaseModel):
    title: str = ""
    is_private: bool = False
    is_protected: bool = False


class TableCreateResponse(TableCreate, BaseForm):
    pass


class AttributeSecondaryCreateBase(BaseModel):
    name: str = ""
    ukr_name: str = ""
    data_type_id: int = 1
    is_unique: bool = False
    is_nullable: bool = False


class AttributeSecondaryCreate(AttributeSecondaryCreateBase):
    table_id: int


class AttributeSecondaryCreateResponse(AttributeSecondaryCreateBase, BaseForm):
    table: Table
    data_types: list[DataType] = []


class RowCreateResponse(BaseForm):
    table: Table
    attributes: list[Attribute]
    values: dict[str, Any] = {}


class RowUpdateResponse(BaseForm):
    table: Table
    attributes: list[Attribute]
    row_id: int
    values: dict[str, Any] = {}

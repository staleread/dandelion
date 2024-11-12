from pydantic import BaseModel

from ..data.models import Table, Attribute, AttributeRich, DataType


class LoginPageContext(BaseModel):
    username: str = ""
    errors: dict[str, str] = {}


class HomePageContext(BaseModel):
    username: str


class TablesViewContext(BaseModel):
    tables: list[Table]


class TableRowsContext(BaseModel):
    table: Table
    attributes: list[Attribute] = []
    rows: list[dict] = []


class TableAttributesContext(BaseModel):
    table: Table
    rows: list[AttributeRich] = []


class TableCreateContext(BaseModel):
    title: str = ""
    is_private: bool = False
    is_protected: bool = False
    errors: dict[str, str] = {}


class AttributeCreateContext(BaseModel):
    table: Table
    name: str = ""
    ukr_name: str = ""
    data_type_id: int = 1
    is_unique: bool = False
    is_nullable: bool = False
    data_types: list[DataType] = []
    errors: dict[str, str] | None = None

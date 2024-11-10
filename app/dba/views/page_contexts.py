from pydantic import BaseModel

from ..data.models import Table, Attribute


class LoginPageContext(BaseModel):
    username: str = ""
    errors: dict[str, str] | None = None


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
    columns: list[dict] = []
    rows: list[Attribute] = []


class TableCreateContext(BaseModel):
    title: str = ""
    is_private: bool = False
    is_protected: bool = False
    errors: dict[str, str] | None = None

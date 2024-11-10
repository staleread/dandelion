from enum import StrEnum


class DbaTemplate(StrEnum):
    LOGIN = "dba/forms/login.html"
    HOME = "dba/home.html"
    TABLES = "dba/tables/tables.html"
    TABLE_ROWS = "dba/tables/table_rows.html"
    TABLE_ATTRIBUTES = "dba/tables/table_attributes.html"
    TABLE_NEW = "dba/forms/table_new.html"
    ATTRIBUTE_NEW = "dba/forms/attribute_new.html"
    INTERNAL_ERROR = "dba/errors/internal.html"
    UNAUTHORIZED_ERROR = "dba/errors/unauthorized.html"
    NOT_FOUND_ERROR = "dba/errors/not_found.html"

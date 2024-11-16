from enum import StrEnum


class Permissions(StrEnum):
    CAN_CONNECT = "can_connect"
    CAN_READ_PUBLIC = "can_read_public"
    CAN_MODIFY_RECORDS = "can_modify_records"
    CAN_MODIFY_ATTRIBUTES = "can_modify_attributes"
    CAN_ADD_USER = "can_add_user"
    CAN_ADD_OPERATOR = "can_add_operator"
    CAN_READ_PRIVATE = "can_read_private"
    CAN_MODIFY_TABLES = "can_modify_tables"
    CAN_ADD_ADMIN = "can_add_admin"

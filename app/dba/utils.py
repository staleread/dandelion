from pydantic import ValidationError


def extract_error_messages(e: ValidationError) -> dict:
    error_dict = {}
    for error in e.errors():
        field = str(error["loc"][0])
        message = error["msg"]
        if field not in error_dict:
            error_dict[field + "_error"] = message
    return error_dict

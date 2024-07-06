from requests import Response

from clickhouse_orm.common.enums import ErrorCodesEnum
from clickhouse_orm.common.errors import UndefinedFieldException


def error_handler(func):
    def wrapper(*args, **kwargs):
        result: Response = func(*args, **kwargs)
        if "X-ClickHouse-Exception-Code" in result.headers:
            match result.headers["X-ClickHouse-Exception-Code"]:
                case ErrorCodesEnum.undefined_field.value:
                    raise UndefinedFieldException
        return result.text.split("\n")

    return wrapper

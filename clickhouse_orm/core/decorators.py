from clickhouse_orm.common.enums import ErrorCodesEnum
from clickhouse_orm.common.errors import UndefinedFieldException


def error_handler(func):
    def wrapper(*args, **kwargs):
        result: list[str] = func(*args, **kwargs)
        if len(result) > 0 and result[0].startswith("Code"):
            match result[0]:
                case ErrorCodesEnum.undefined_field.value:
                    print(result[0])
        return result

    return wrapper

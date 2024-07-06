from clickhouse_orm.model import Model
from clickhouse_orm.core.connector import ClickHouseConnector


class User(Model):
    __table__ = "user"


ch = ClickHouseConnector(
    host="localhost",
    user="test",
    password="test"
)

print(ch.all(User, "name", "age", "sex", "lex", "dex"))


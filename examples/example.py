from clickhouse_orm.models import Model
from clickhouse_orm.core.connector import ClickHouseConnector


class User(Model):
    __table__ = "user"


ch = ClickHouseConnector(
    host="localhost",
    user="test",
    password="test"
)

try:
    print(ch.all(User, "name", "id", "age"))
except Exception as e:
    print(str(e))


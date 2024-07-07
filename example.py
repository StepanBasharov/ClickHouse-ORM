from clickhouse_orm.models import Model
from clickhouse_orm.fields import (
    IntField,
    CharField
)
from clickhouse_orm.core.connector import ClickHouseConnector


class User(Model):
    __table__ = "user"
    id = IntField()
    name = CharField()
    age = IntField()
    salary = IntField()


ch = ClickHouseConnector(
    host="localhost",
    user="test",
    password="test"
)
data = ch.all(User)

for i in data:
    print(f"{i.id} - {i.name} - {i.age} - {i.salary}")


from typing import Type

import requests

from clickhouse_orm.model import Model
from clickhouse_orm.core.decorators import error_handler


class ClickHouseConnector:
    def __init__(
            self,
            host: str,
            port: int = 8123,
            database: str = "default",
            user: str = None,
            password: str = None,
            use_tls: bool = False
    ):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.use_tls = use_tls
        self.headers: dict = dict()
        self.dsn = None
        self._build_dsn()

    def _build_dsn(self):
        if self.use_tls:
            dsn = f"https://{self.host}:{self.port}"
        else:
            dsn = f"http://{self.host}:{self.port}"

        if self.user:
            self.headers['X-ClickHouse-User'] = self.user
        if self.password:
            self.headers['X-ClickHouse-Key'] = self.password
        self.headers['X-ClickHouse-Database'] = self.database

        self.dsn = dsn

    def _commit(self, query: str):
        url = f"{self.dsn}/?query={query}"
        ch_response = requests.get(url=url, headers=self.headers)
        return ch_response.text.split("\n")

    @error_handler
    def all(self, model: Type[Model], *args):
        columns = []
        if len(args) > 0:
            for column in args:
                columns.append(column)
        if len(columns) > 0:
            query = f"SELECT {", ".join(columns)} FROM {model.__table__};"
        else:
            query = f"SELECT * FROM {model.__table__};"
        return self._commit(query=query)

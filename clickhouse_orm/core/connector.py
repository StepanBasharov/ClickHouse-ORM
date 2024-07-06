from typing import Type

import requests
from requests import Response

from clickhouse_orm.models import Model
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
        self.dsn = self._build_dsn()

    def _build_dsn(self) -> str:
        """ Создать интерфейс соединения с базой данных """
        if self.use_tls:
            dsn = f"https://{self.host}:{self.port}"
        else:
            dsn = f"http://{self.host}:{self.port}"

        if self.user:
            self.headers['X-ClickHouse-User'] = self.user
        if self.password:
            self.headers['X-ClickHouse-Key'] = self.password
        self.headers['X-ClickHouse-Database'] = self.database

        return dsn

    @error_handler
    def _commit(self, query: str) -> Response:
        """ Отправить запрос базе """
        url = f"{self.dsn}/?query={query}"
        ch_response = requests.get(url=url, headers=self.headers)
        return ch_response

    def all(self, model: Type[Model], *args):
        """ Получить все записи таблицы"""
        columns = []
        if len(args) > 0:
            for column in args:
                columns.append(column)
        if len(columns) > 0:
            query = f"SELECT {", ".join(columns)} FROM {model.__table__};"
        else:
            query = f"SELECT * FROM {model.__table__};"
        return self._commit(query=query)

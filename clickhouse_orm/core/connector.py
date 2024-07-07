import json
from copy import copy
from json import JSONDecodeError
from typing import Type

import requests
from requests import Response

from clickhouse_orm.fields import IntField, Field
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
        """ Create Interface for connection to ClickHouse """
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
        """ Create Commit to Database """
        url = f"{self.dsn}/?query={query}"
        ch_response = requests.get(url=url, headers=self.headers)
        return ch_response

    def _remove_python_vars(self, python_vars: dict):
        python_vars.pop("__table__")
        python_vars.pop("__doc__")
        return python_vars

    def all(self, model: Type[Model], *args) -> list:
        """
        Get all objects from table
        model: table model class
        *args: fields for get
        """
        objects = []
        columns = []
        if len(args) > 0:
            for column in args:
                columns.append(column)
        if len(columns) > 0:
            query = f"SELECT {", ".join(columns)} FROM {model.__table__} FORMAT JSONEachRow;"
        else:
            query = f"SELECT * FROM {model.__table__} FORMAT JSONEachRow;"
        rows = self._commit(query=query)
        for row in rows:
            row = row.replace("'", "\"")
            try:
                row = json.loads(row)
            except JSONDecodeError:
                continue
            new_model = model()
            fields = self._remove_python_vars(dict(vars(model)))
            for key in row:
                data: Field = fields[key]
                data = copy(data)
                data.to_python_type(row[key])
                setattr(new_model, key, data)

            objects.append(new_model)

        return objects

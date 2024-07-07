from typing import Any


class Field:
    __value__ = None

    def __init__(self, data=None):
        if data:
            __value__ = self.to_python_type(data)

    @staticmethod
    def to_python_type(data) -> Any:
        ...

    def create_new(self, data):
        ...

    def __repr__(self):
        return str(self.__value__)

    def __str__(self):
        return str(self.__value__)


class IntField(Field):
    __value__ = None

    def to_python_type(self, data: str):
        self.__value__ = int(data)


class CharField(Field):
    __value__ = None

    def to_python_type(self, data):
        self.__value__ = str(data)

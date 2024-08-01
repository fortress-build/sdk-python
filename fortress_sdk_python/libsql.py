from .database import (
    DatabaseClient,
    ConnectionInterface,
    CursorInterface,
)
import libsql_experimental as libsql
from typing import Any


class LibsqlCursor(CursorInterface):
    def __init__(self, cursor):
        self.__cursor = cursor
        self.arraysize = self.__cursor.arraysize

    @property
    def description(self) -> tuple[tuple[Any, ...], ...] | None:
        return self.__cursor.description

    @property
    def rowcount(self) -> int:
        return self.__cursor.rowcount

    @property
    def lastrowid(self) -> int | None:
        return self.__cursor.lastrowid

    def execute(self, sql: str, parameters: tuple[Any] = ...) -> "LibsqlCursor":
        return LibsqlCursor(self.__cursor.execute(sql, parameters))

    def executemany(
        self, sql: str, parameters: list[tuple[Any]] = ...
    ) -> "LibsqlCursor":
        return LibsqlCursor(self.__cursor.executemany(sql, parameters))

    def fetchone(self) -> tuple[Any] | None:
        return self.__cursor.fetchone()

    def fetchmany(self, size: int = ...) -> list[tuple[Any, ...]]:
        return self.__cursor.fetchmany(size)

    def fetchall(self) -> list[tuple[Any]]:
        return self.__cursor.fetchall()


class LibsqlConnection(ConnectionInterface):
    def __init__(self, connection):
        self.__connection = connection
        self.in_transaction: bool = self.__connection.in_transaction

    def commit(self) -> None:
        return self.__connection.commit()

    def cursor(self) -> LibsqlCursor:
        return self.__connection.cursor()

    def sync(self) -> None:
        return self.__connection.sync()

    def rollback(self) -> None:
        return self.__connection.rollback()

    def execute(self, sql: str, parameters: tuple[Any] = ...) -> LibsqlCursor:
        return self.__connection.execute(sql, parameters)

    def executemany(self, sql: str, parameters: list[tuple[Any]] = ...) -> LibsqlCursor:
        return self.__connection.executemany(sql, parameters)

    def executescript(self, script: str) -> None:
        return self.__connection.executescript(script)


class LibsqlClient(DatabaseClient):
    def __init__(self, url: str, token: str) -> None:
        self.__url = url
        self.__token = token

    def connect(self) -> LibsqlConnection:

        return LibsqlConnection(
            libsql.connect(
                database=self.__url,
                auth_token=self.__token,
            )
        )

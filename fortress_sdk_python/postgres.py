from .database import (
    DatabaseClient,
    Connection,
    Cursor,
)
import psycopg2
from typing import Any


class PostgresCursor(Cursor):
    def __init__(self, cursor):
        self.__cursor = cursor

    @property
    def description(self) -> tuple[tuple[Any, ...], ...] | None:
        return self.__cursor.description

    @property
    def rowcount(self) -> int:
        return self.__cursor.rowcount

    @property
    def lastrowid(self) -> int | None:
        return self.__cursor.lastrowid

    def execute(self, sql: str, parameters: tuple[Any] = ...) -> "PostgresCursor":
        self.__cursor.execute(sql, parameters)
        return PostgresCursor(self.__cursor)

    def executemany(
        self, sql: str, parameters: list[tuple[Any]] = ...
    ) -> "PostgresCursor":
        self.__cursor.executemany(sql, parameters)
        return PostgresCursor(self.__cursor)

    def fetchone(self) -> tuple[Any] | None:
        return self.__cursor.fetchone()

    def fetchmany(self, size: int = ...) -> list[tuple[Any, ...]]:
        return self.__cursor.fetchmany(size)

    def fetchall(self) -> list[tuple[Any]]:
        return self.__cursor.fetchall()

    def __enter__(self) -> "PostgresCursor":
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.__cursor.__exit__(exc_type, exc_value, traceback)


class PostgresConnection(Connection):
    def __init__(self, connection: psycopg2.extensions.connection):
        self.__connection = connection
        self.isolation_level: str = self.__connection.isolation_level

    def commit(self) -> None:
        return self.__connection.commit()

    def cursor(self) -> PostgresCursor:
        return PostgresCursor(self.__connection.cursor())

    def sync(self) -> None:
        return self.__connection.sync()

    def rollback(self) -> None:
        return self.__connection.rollback()

    def fetchall(self, sql: str, parameters: tuple[Any] = ...) -> list[tuple[Any]]:
        return self.__connection.fetchall(sql, parameters)

    def executemany(
        self, sql: str, parameters: list[tuple[Any]] = ...
    ) -> PostgresCursor:
        return self.__connection.executemany(sql, parameters)

    def executescript(self, script: str) -> None:
        return self.__connection.executescript(script)


class PostgresClient(DatabaseClient):
    def __init__(
        self, host: str, port: int, user: str, password: str, database_name: str
    ) -> None:
        self.__host = host
        self.__port = port
        self.__user = user
        self.__password = password
        self.__database_name = database_name

    def connect(self) -> PostgresConnection:
        return PostgresConnection(
            psycopg2.connect(
                f"dbname={self.__database_name} user={self.__user} password={self.__password} host={self.__host} port={self.__port} sslmode=disable"
            )
        )

from typing import Any


class Cursor:
    def __init__(self, cursor):
        self.__cursor: "Cursor" = NotImplementedError
        self.arraysize: int = NotImplementedError

    @property
    def description(self) -> tuple[tuple[Any, ...], ...] | None:
        raise NotImplementedError

    @property
    def rowcount(self) -> int:
        raise NotImplementedError

    @property
    def lastrowid(self) -> int | None:
        raise NotImplementedError

    def execute(self, sql: str, parameters: tuple[Any] = ...) -> "Cursor":
        raise NotImplementedError

    def executemany(self, sql: str, parameters: list[tuple[Any]] = ...) -> "Cursor":
        raise NotImplementedError

    def fetchone(self) -> tuple[Any] | None:
        raise NotImplementedError

    def fetchmany(self, size: int = ...) -> list[tuple[Any, ...]]:
        raise NotImplementedError

    def fetchall(self) -> list[tuple[Any]]:
        raise NotImplementedError

    def __enter__(self) -> "Cursor":
        raise NotImplementedError

    def __exit__(self, exc_type, exc_value, traceback):
        raise NotImplementedError


class Connection:
    def __init__(self, connection):
        self.in_transaction: bool = NotImplementedError
        self.isolation_level: str = NotImplementedError

    def commit(self) -> None:
        raise NotImplementedError

    def cursor(self) -> Cursor:
        raise NotImplementedError

    def sync(self) -> None:
        raise NotImplementedError

    def rollback(self) -> None:
        raise NotImplementedError

    def execute(self, sql: str, parameters: tuple[Any] = ...) -> Cursor:
        raise NotImplementedError

    def executemany(self, sql: str, parameters: list[tuple[Any]] = ...) -> Cursor:
        raise NotImplementedError

    def executescript(self, script: str) -> None:
        raise NotImplementedError


class DatabaseClient:
    def __init__(self) -> None:
        """Initialize the Database client"""
        raise NotImplementedError

    def connect(self) -> Connection:
        """Connect return an active connection to the database"""
        raise NotImplementedError

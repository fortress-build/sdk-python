from typing import Any


class CursorInterface:
    def __init__(self, cursor):
        self.__cursor: "CursorInterface" = NotImplementedError
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

    def execute(self, sql: str, parameters: tuple[Any] = ...) -> "CursorInterface":
        raise NotImplementedError

    def executemany(
        self, sql: str, parameters: list[tuple[Any]] = ...
    ) -> "CursorInterface":
        raise NotImplementedError

    def fetchone(self) -> tuple[Any] | None:
        raise NotImplementedError

    def fetchmany(self, size: int = ...) -> list[tuple[Any, ...]]:
        raise NotImplementedError

    def fetchall(self) -> list[tuple[Any]]:
        raise NotImplementedError


class ConnectionInterface:
    def __init__(self, connection):
        self.__connection: "ConnectionInterface" = ...
        self.in_transaction: bool = ...

    def commit(self) -> None:
        raise NotImplementedError

    def cursor(self) -> CursorInterface:
        raise NotImplementedError

    def sync(self) -> None:
        raise NotImplementedError

    def rollback(self) -> None:
        raise NotImplementedError

    def execute(self, sql: str, parameters: tuple[Any] = ...) -> CursorInterface:
        raise NotImplementedError

    def executemany(
        self, sql: str, parameters: list[tuple[Any]] = ...
    ) -> CursorInterface:
        raise NotImplementedError

    def executescript(self, script: str) -> None:
        raise NotImplementedError


class DatabaseClient:
    def __init__(self) -> None:
        """Initialize the Database client"""
        raise NotImplementedError

    def connect(self) -> ConnectionInterface:
        """Connect return an active connection to the database"""
        raise NotImplementedError

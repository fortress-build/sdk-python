from .fortress import (
    DatabaseCreateResponse,
    DatabaseDeleteResponse,
    DatabaseListResponse,
    Fortress,
)
from .database import ConnectionInterface
from .libsql import LibsqlClient


class Client:
    def __init__(self, org_id: str, api_key: str) -> None:
        """Initialize the Fortress client"""
        if not org_id:
            raise ValueError("Organization ID is required")
        if not api_key:
            raise ValueError("API Key is required")

        self.__fortress = Fortress(org_id, api_key)

    def connect(self, database_name: str) -> ConnectionInterface:
        """Connect to a database on the Fortress platform"""
        response = self.__fortress.get_uri(database_name)
        if not response.success:
            raise ValueError(response.message)

        return LibsqlClient(
            url=response.url,
            token=response.token,
        ).connect()

    def create_database(self, database_name: str) -> DatabaseCreateResponse:
        """Create a new database on the Fortress platform"""
        return self.__fortress.create_database(database_name)

    def delete_database(self, database_name: str) -> DatabaseDeleteResponse:
        """Delete a database on the Fortress platform"""
        return self.__fortress.delete_database(database_name)

    def list_databases(self) -> DatabaseListResponse:
        """List all databases on the Fortress platform"""
        return self.__fortress.list_databases()

from .client import (
    Database,
    Tenant,
    Client,
)
from .database import Connection
from .postgres import PostgresClient, PostgresConnection


class Fortress:
    def __init__(self, org_id: str, api_key: str) -> None:
        """Initialize the Fortress client"""
        if not org_id:
            raise ValueError("Organization ID is required")
        if not api_key:
            raise ValueError("API Key is required")

        self.__fortress = Client(org_id, api_key)
        self.__connection_cache = {}
        self.__tenant_to_database = {}

    def connect_database(self, database_id: str) -> Connection:
        """
        Connect to a database on the Fortress platform

        :param database_id: ID of the database
        :return: Connection object to the database
        """
        if database_id in self.__connection_cache:
            return self.__connection_cache[database_id]

        response = self.__fortress.get_uri(database_id, "database")

        connection = PostgresClient(
            response.url,
            response.port,
            response.username,
            response.password,
            response.database,
        ).connect()

        self.__connection_cache[database_id] = connection
        return connection

    def create_database(self, alias: str = "") -> str:
        """
        Create a new database on the Fortress platform
        Returns the ID of the created

        :param alias: Alias for the database (optional)
        """
        return self.__fortress.create_database(alias=alias)

    def delete_database(self, database_id: str) -> None:
        """
        Delete a database on the Fortress platform

        :param database_id: ID of the database to delete
        """
        self.__fortress.delete_database(database_id=database_id)

    def list_databases(self) -> list[Database]:
        """
        List all databases on the Fortress platform

        :return: List of databases
        """
        return self.__fortress.list_databases()

    def connect_tenant(self, tenant_id: str) -> Connection:
        """
        Connect to a tenant's database on the Fortress platform

        :param tenant_id: ID of the tenant
        :return: Connection object to the tenant's database
        """
        if tenant_id in self.__tenant_to_database:
            return self.connect_database(
                self.__connection_cache[self.__tenant_to_database[tenant_id]]
            )

        response = self.__fortress.get_uri(tenant_id, "tenant")

        connection = PostgresClient(
            response.url,
            response.port,
            response.username,
            response.password,
            response.database,
        ).connect()

        self.__tenant_to_database[tenant_id] = response.database_id
        self.__connection_cache[response.database_id] = connection
        return connection

    def create_tenant(
        self, tenant_id: str, alias: str = "", database_id: str = ""
    ) -> None:
        """
        Create a new tenant on the Fortress platform

        :param tenant_id: ID of the tenant
        :param alias: Alias for the tenant (optional)
        :param database_id: ID of the database to assign the tenant to or if not provided a database will be created (optional)
        """
        self.__fortress.create_tenant(
            tenant_id=tenant_id, alias=alias, database_id=database_id
        )

    def delete_tenant(self, tenant_id: str) -> None:
        """
        Delete a tenant on the Fortress platform

        :param tenant_id: ID of the tenant to delete
        """
        self.__fortress.delete_tenant(tenant_id=tenant_id)

    def list_tenants(self) -> list[Tenant]:
        """
        List all tenants on the Fortress platform

        :return: List of tenants
        """
        return self.__fortress.list_tenants()

from .fortress import (
    DatabaseCreateResponse,
    DatabaseDeleteResponse,
    DatabaseListResponse,
    TenantCreateResponse,
    TenantDeleteResponse,
    TenantListResponse,
    Fortress,
)
from .database import ConnectionInterface
from .postgres import PostgresClient, PostgresConnection


class Client:
    def __init__(self, org_id: str, api_key: str) -> None:
        """Initialize the Fortress client"""
        if not org_id:
            raise ValueError("Organization ID is required")
        if not api_key:
            raise ValueError("API Key is required")

        self.__fortress = Fortress(org_id, api_key)

    def connect_database(self, database_id: str) -> ConnectionInterface:
        """Connect to a database on the Fortress platform"""
        response = self.__fortress.get_uri(database_id, "database")
        if not response.success:
            raise ValueError(response.message)

        return PostgresConnection(
            response.url,
            response.port,
            response.username,
            response.password,
            response.database,
        )

    def create_database(self, alias: str) -> DatabaseCreateResponse:
        """Create a new database on the Fortress platform"""
        return self.__fortress.create_database(alias=alias)

    def delete_database(self, database_id: str) -> DatabaseDeleteResponse:
        """Delete a database on the Fortress platform"""
        return self.__fortress.delete_database(database_id=database_id)

    def list_databases(self) -> DatabaseListResponse:
        """List all databases on the Fortress platform"""
        return self.__fortress.list_databases()

    def connect_tenant(self, tenant_name: str) -> ConnectionInterface:
        """Connect to a tenant's database on the Fortress platform"""
        response = self.__fortress.get_uri(tenant_name, "tenant")
        if not response.success:
            raise ValueError(response.message)

        return PostgresClient(
            response.url,
            response.port,
            response.username,
            response.password,
            response.database,
        ).connect()

    def create_tenant(
        self, tenant_name: str, alias: str, database_id: str = ""
    ) -> TenantCreateResponse:
        """Create a new tenant on the Fortress platform"""
        return self.__fortress.create_tenant(
            tenant_name=tenant_name, alias=alias, database_id=database_id
        )

    def delete_tenant(self, tenant_name: str) -> TenantDeleteResponse:
        """Delete a tenant on the Fortress platform"""
        return self.__fortress.delete_tenant(tenant_name=tenant_name)

    def list_tenants(self) -> TenantListResponse:
        """List all tenants on the Fortress platform"""
        return self.__fortress.list_tenants()

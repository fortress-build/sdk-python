import json
import requests
from dataclasses import dataclass
import datetime
from .crypto import decrypt


@dataclass
class Database:
    id: str
    alias: str
    size: int
    average_read_iops: int
    average_write_iops: int
    date_created: datetime.datetime


@dataclass
class Tenant:
    name: str
    alias: str
    database_id: str
    date_created: datetime.datetime


@dataclass
class TenantListResponse:
    success: bool
    message: str
    tenants: list[Tenant]


@dataclass
class TenantCreateResponse:
    success: bool
    message: str


@dataclass
class TenantDeleteResponse:
    success: bool
    message: str


@dataclass
class DatabaseListResponse:
    success: bool
    message: str
    databases: list[Database]


@dataclass
class DatabaseCreateResponse:
    success: bool
    message: str
    id: str


@dataclass
class DatabaseDeleteResponse:
    success: bool
    message: str


@dataclass
class DatabaseUriResponse:
    success: bool
    message: str
    url: str
    database: str
    port: int
    username: str
    password: str


class Fortress:
    def __init__(
        self,
        org_id: str,
        api_key: str,
    ):
        self.base_url = "https://api.fortress.build"
        self.org_id = org_id
        self.api_key = api_key

    def get_uri(self, id: str, type: str) -> DatabaseUriResponse:
        if type != "tenant" and type != "database":
            return DatabaseUriResponse(
                success=False,
                message="Invalid type",
                url="",
                database="",
                port=0,
                username="",
                password="",
            )

        endpoint = f"{self.base_url}/v1/organization/{self.org_id}/{type}/{id}/uri"
        response = requests.get(
            endpoint,
            headers={"Api-Key": self.api_key},
        )

        json_response = response.json()
        if response.status_code != 200:
            return DatabaseUriResponse(
                success=False,
                message=json_response.get("message", "An error occured"),
                url="",
                database="",
                port=0,
                username="",
                password="",
            )

        connection_details_str = None
        try:
            connection_details_str = decrypt(
                private_key=self.api_key,
                ciphertext=json_response.get("connectionDetails", ""),
            )
        except Exception as e:
            return DatabaseUriResponse(
                success=False,
                message=f"An error occured while decrypting the database URI: {str(e)}",
                url="",
                database="",
                port=0,
                username="",
                password="",
            )

        if connection_details_str is None:
            return DatabaseUriResponse(
                success=False,
                message="An error occured",
                url="",
                database="",
                port=0,
                username="",
                password="",
            )

        connection_details = json.loads(connection_details_str)
        url = connection_details.get("url", "")
        database = connection_details.get("database", "")
        port = int(connection_details.get("port", 0))
        username = connection_details.get("username", "")
        password = connection_details.get("password", "")

        if url == "" or port == 0 or username == "" or password == "" or database == "":
            return DatabaseUriResponse(
                success=False,
                message="An error occured",
                url="",
                database="",
                port=0,
                username="",
                password="",
            )

        return DatabaseUriResponse(
            success=True,
            message=json_response["message"],
            url=url,
            database=database,
            port=port,
            username=username,
            password=password,
        )

    def create_database(self, alias: str) -> DatabaseCreateResponse:
        endpoint = f"{self.base_url}/v1/organization/{self.org_id}/database"
        payload = {"alias": alias}
        response = requests.post(
            endpoint,
            headers={"Api-Key": self.api_key},
            json=payload,
        )

        json_response = response.json()
        if response.status_code != 200:
            return DatabaseCreateResponse(
                success=False,
                message=json_response.get("message", "An error occured"),
                id=json_response.get("databaseId", ""),
            )

        return DatabaseCreateResponse(
            success=True,
            message=json_response["message"],
            id=json_response["databaseId"],
        )

    def delete_database(self, database_id: str) -> DatabaseDeleteResponse:
        endpoint = (
            f"{self.base_url}/v1/organization/{self.org_id}/database/{database_id}"
        )
        response = requests.delete(
            endpoint,
            headers={"Api-Key": self.api_key},
        )

        json_response = response.json()
        if response.status_code != 200:
            return DatabaseDeleteResponse(
                success=False,
                message=json_response.get("message", "An error occured"),
            )

        return DatabaseDeleteResponse(
            success=True,
            message=json_response["message"],
        )

    def list_databases(self) -> DatabaseListResponse:
        endpoint = f"{self.base_url}/v1/organization/{self.org_id}/databases"
        response = requests.get(
            endpoint,
            headers={"Api-Key": self.api_key},
        )

        json_response = response.json()
        if response.status_code != 200:
            return DatabaseListResponse(
                success=False,
                message=json_response.get("message", "An error occured"),
                databases=[],
            )

        databases = [
            Database(
                id=data.get("databaseId", ""),
                alias=data.get("alias", ""),
                size=data.get("sizeBytes", 0),
                average_read_iops=data.get("averageReadIOPS", 0),
                average_write_iops=data.get("averageWriteIOPS", 0),
                date_created=datetime.datetime.fromisoformat(
                    data.get("createdDate", "")
                ),
            )
            for data in json_response.get("databases", [])
        ]

        return DatabaseListResponse(
            success=True,
            message=json_response.get("message", "An error occured"),
            databases=databases,
        )

    def create_tenant(
        self, tenant_name: str, alias: str, database_id: str = ""
    ) -> TenantCreateResponse:
        endpoint = f"{self.base_url}/v1/organization/{self.org_id}/tenant/{tenant_name}"
        payload = {"alias": alias}
        if database_id:
            payload["databaseId"] = database_id

        response = requests.post(
            endpoint,
            headers={"Api-Key": self.api_key},
            json=payload,
        )

        json_response = response.json()
        if response.status_code != 200:
            return TenantCreateResponse(
                success=False,
                message=json_response.get(
                    "message", json_response.get("message", "An error occured")
                ),
            )

        return TenantCreateResponse(
            success=True,
            message=json_response["message"],
        )

    def delete_tenant(self, tenant_name: str) -> TenantDeleteResponse:
        endpoint = f"{self.base_url}/v1/organization/{self.org_id}/tenant/{tenant_name}"
        response = requests.delete(
            endpoint,
            headers={"Api-Key": self.api_key},
        )

        json_response = response.json()
        if response.status_code != 200:
            return TenantDeleteResponse(
                success=False,
                message=json_response.get("message", "An error occured"),
            )

        return TenantDeleteResponse(
            success=True,
            message=json_response["message"],
        )

    def list_tenants(self) -> TenantListResponse:
        endpoint = f"{self.base_url}/v1/organization/{self.org_id}/tenants"
        response = requests.get(
            endpoint,
            headers={"Api-Key": self.api_key},
        )

        json_response = response.json()
        if response.status_code != 200:
            return TenantListResponse(
                success=False,
                message=json_response.get("message", "An error occured"),
                tenants=[],
            )

        tenants = [
            Tenant(
                name=data.get("tenantName", ""),
                alias=data.get("alias", ""),
                database_id=data.get("databaseId", ""),
                date_created=datetime.datetime.fromisoformat(
                    data.get("createdDate", "")
                ),
            )
            for data in json_response.get("tenants", [])
        ]

        return TenantListResponse(
            success=True,
            message=json_response.get("message", "An error occured"),
            tenants=tenants,
        )

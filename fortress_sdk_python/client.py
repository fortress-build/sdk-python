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
    created_date: datetime.datetime


@dataclass
class Tenant:
    id: str
    alias: str
    database_id: str
    created_date: datetime.datetime


@dataclass
class ConnectionDetails:
    database_id: str
    url: str
    database: str
    port: int
    username: str
    password: str


class InternalError(Exception):
    def __init__(self, message="Internal Server Error"):
        self.message = message
        super().__init__(self.message)


class ValidationError(Exception):
    def __init__(self, message="Validation Error"):
        self.message = message
        super().__init__(self.message)


class Client:
    def __init__(
        self,
        org_id: str,
        api_key: str,
    ):
        self.base_url = "https://api.fortress.build"
        self.org_id = org_id
        self.api_key = api_key

    def get_uri(self, id: str, type: str) -> ConnectionDetails:
        if type != "tenant" and type != "database":
            raise ValidationError("Type must be either 'tenant' or 'database'")

        endpoint = f"{self.base_url}/v1/organization/{self.org_id}/{type}/{id}/uri"
        response = requests.get(
            endpoint,
            headers={"Api-Key": self.api_key},
        )

        json_response = response.json()
        if response.status_code != 200:
            if response.status_code == 400:
                raise ValidationError(json_response.get("message", "Validation Error"))
            if response.status_code == 500:
                raise InternalError(
                    json_response.get("message", "Internal Server Error")
                )

        connection_details_str = None
        try:
            connection_details_str = decrypt(
                private_key=self.api_key,
                ciphertext=json_response.get("connectionDetails", ""),
            )
        except Exception as e:
            raise InternalError(
                "An error occured: Unable to decrypt connection details"
            )

        if connection_details_str is None:
            raise InternalError(
                "An error occured: Unable to decrypt connection details"
            )

        connection_details = json.loads(connection_details_str)
        url = connection_details.get("url", "")
        database = connection_details.get("database", "")
        port = int(connection_details.get("port", 0))
        username = connection_details.get("username", "")
        password = connection_details.get("password", "")

        if url == "" or port == 0 or username == "" or password == "" or database == "":
            raise InternalError("An error occured: Invalid connection details")

        return ConnectionDetails(
            database_id=json_response["databaseId"],
            url=url,
            database=database,
            port=port,
            username=username,
            password=password,
        )

    def create_database(self, alias: str = "") -> str:
        endpoint = f"{self.base_url}/v1/organization/{self.org_id}/database"
        payload = {"alias": alias}
        response = requests.post(
            endpoint,
            headers={"Api-Key": self.api_key},
            json=payload,
        )

        json_response = response.json()
        if response.status_code != 200:
            if response.status_code == 400:
                raise ValidationError(json_response.get("message", "Validation Error"))
            if response.status_code == 500:
                raise InternalError(
                    json_response.get("message", "Internal Server Error")
                )

        return json_response["databaseId"]

    def delete_database(self, database_id: str):
        endpoint = (
            f"{self.base_url}/v1/organization/{self.org_id}/database/{database_id}"
        )
        response = requests.delete(
            endpoint,
            headers={"Api-Key": self.api_key},
        )

        json_response = response.json()
        if response.status_code != 200:
            if response.status_code == 400:
                raise ValidationError(json_response.get("message", "Validation Error"))
            if response.status_code == 500:
                raise InternalError(
                    json_response.get("message", "Internal Server Error")
                )

    def list_databases(self) -> list[Database]:
        endpoint = f"{self.base_url}/v1/organization/{self.org_id}/databases"
        response = requests.get(
            endpoint,
            headers={"Api-Key": self.api_key},
        )

        json_response = response.json()
        if response.status_code != 200:
            if response.status_code == 400:
                raise ValidationError(json_response.get("message", "Validation Error"))
            else:
                raise InternalError(
                    json_response.get("message", "Internal Server Error")
                )

        databases = [
            Database(
                id=data.get("databaseId", ""),
                alias=data.get("alias", ""),
                size=data.get("sizeBytes", 0),
                average_read_iops=data.get("averageReadIOPS", 0),
                average_write_iops=data.get("averageWriteIOPS", 0),
                created_date=datetime.datetime.fromisoformat(
                    data.get("createdDate", "")
                ),
            )
            for data in json_response.get("databases", [])
        ]

        return databases

    def create_tenant(
        self, tenant_id: str, alias: str = "", database_id: str = ""
    ) -> None:
        endpoint = f"{self.base_url}/v1/organization/{self.org_id}/tenant/{tenant_id}"
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
            if response.status_code == 400:
                raise ValidationError(json_response.get("message", "Validation Error"))
            if response.status_code == 500:
                raise InternalError(
                    json_response.get("message", "Internal Server Error")
                )

    def delete_tenant(self, tenant_id: str) -> None:
        endpoint = f"{self.base_url}/v1/organization/{self.org_id}/tenant/{tenant_id}"
        response = requests.delete(
            endpoint,
            headers={"Api-Key": self.api_key},
        )

        json_response = response.json()
        if response.status_code != 200:
            if response.status_code == 400:
                raise ValidationError(json_response.get("message", "Validation Error"))
            if response.status_code == 500:
                raise InternalError(
                    json_response.get("message", "Internal Server Error")
                )

    def list_tenants(self) -> list[Tenant]:
        endpoint = f"{self.base_url}/v1/organization/{self.org_id}/tenants"
        response = requests.get(
            endpoint,
            headers={"Api-Key": self.api_key},
        )

        json_response = response.json()
        if response.status_code != 200:
            if response.status_code == 400:
                raise ValidationError(json_response.get("message", "Validation Error"))
            else:
                raise InternalError(
                    json_response.get("message", "Internal Server Error")
                )

        tenants = [
            Tenant(
                name=data.get("tenantId", ""),
                alias=data.get("alias", ""),
                database_id=data.get("databaseId", ""),
                created_date=datetime.datetime.fromisoformat(
                    data.get("createdDate", "")
                ),
            )
            for data in json_response.get("tenants", [])
        ]

        return tenants

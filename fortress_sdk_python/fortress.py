import requests
from dataclasses import dataclass
from .crypto import decrypt


@dataclass
class Database:
    id: str
    name: str
    size: int
    rows_read: int
    rows_written: int


@dataclass
class DatabaseListResponse:
    success: bool
    message: str
    databases: list[Database]


@dataclass
class DatabaseCreateResponse:
    success: bool
    message: str


@dataclass
class DatabaseDeleteResponse:
    success: bool
    message: str


@dataclass
class DatabaseUriResponse:
    success: bool
    message: str
    url: str
    token: str


class Fortress:
    def __init__(
        self,
        org_id: str,
        api_key: str,
    ):
        self.base_url = "https://api.fortress.build/api"
        self.org_id = org_id
        self.api_key = api_key

    def get_uri(self, database):
        endpoint = (
            f"{self.base_url}/v1/organization/{self.org_id}/{database}/database/uri"
        )
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
                token="",
            )

        url = None
        token = None
        try:
            url = decrypt(
                private_key=self.api_key,
                ciphertext=json_response.get("url", ""),
            )
            token = decrypt(
                private_key=self.api_key,
                ciphertext=json_response.get("token", ""),
            )
        except Exception as e:
            return DatabaseUriResponse(
                success=False,
                message=f"An error occured while decrypting the database URI: {str(e)}",
                url="",
                token="",
            )

        if url is None or token is None:
            return DatabaseUriResponse(
                success=False,
                message="An error occured",
                url="",
                token="",
            )

        return DatabaseUriResponse(
            success=True,
            message=json_response["message"],
            url=url,
            token=token,
        )

    def create_database(self, database):
        endpoint = f"{self.base_url}/v1/organization/{self.org_id}/{database}/database"
        response = requests.post(
            endpoint,
            headers={"Api-Key": self.api_key},
        )

        json_response = response.json()
        if response.status_code != 200:
            return DatabaseCreateResponse(
                success=False,
                message=json_response.get(
                    "message", json_response.get("message", "An error occured")
                ),
            )

        return DatabaseCreateResponse(
            success=True,
            message=json_response["message"],
        )

    def delete_database(self, database):
        endpoint = f"{self.base_url}/v1/organization/{self.org_id}/{database}/database"
        response = requests.delete(
            endpoint,
            headers={"Api-Key": self.api_key},
        )

        json_response = response.json()
        if response.status_code != 200:
            return DatabaseDeleteResponse(
                success=False,
                message=json_response.get("message", "An error occured"),
                databases=[],
            )

        return DatabaseDeleteResponse(
            success=True,
            message=json_response["message"],
        )

    def list_databases(self):
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
                id=data.get("id", ""),
                name=data.get("name", ""),
                size=data.get("size", 0),
                rows_read=data.get("rows_read", 0),
                rows_written=data.get("rows_written", 0),
            )
            for data in json_response.get("databases", [])
        ]

        return DatabaseListResponse(
            success=True,
            message="Success",
            databases=databases,
        )

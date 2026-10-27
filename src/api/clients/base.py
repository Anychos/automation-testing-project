from typing import Any
from httpx import URL, Client, QueryParams, Response


class BaseAPIClient:
    def __init__(self, client: Client) -> None:
        self.client = client

    def close(self) -> None:
        self.client.close()

    def get(self, *, url: str | URL, params: QueryParams | None = None, headers: dict[str, str] | None = None) -> Response:
        return self.client.get(url=url, params=params, headers=headers)

    def post(self, *, url: str | URL, params: QueryParams | None = None, headers: dict[str, str] | None = None, json: Any | None = None) -> Response:
        return self.client.post(url=url, params=params, headers=headers, json=json)

    def patch(self, *, url: str | URL, params: QueryParams | None = None, headers: dict[str, str] | None = None, json: Any | None = None) -> Response:
        return self.client.post(url=url, params=params, headers=headers, json=json)

    def delete(self, *, url: str | URL, params: QueryParams | None = None, headers: dict[str, str] | None = None) -> Response:
        return self.client.post(url=url, params=params, headers=headers)
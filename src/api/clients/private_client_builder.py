from httpx import Client

from config import settings
from src.api.clients.auth import AuthAPIClient
from src.api.schemas.auth import LoginRequestSchema


def private_client_builder(
    auth_client: AuthAPIClient, login_data: LoginRequestSchema
) -> Client:
    login_response = auth_client.login(json=login_data)

    token = login_response.access_token

    return Client(
        base_url=settings.client_settings.url,
        timeout=settings.client_settings.timeout,
        headers={"Authorization": f"Bearer {token}"},
    )

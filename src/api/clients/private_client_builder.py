from httpx import Client

from api.clients.auth import AuthAPIClient
from api.schemas.auth import LoginRequestSchema


def private_client_builder(auth_client: AuthAPIClient, login_data: LoginRequestSchema) -> Client:
    login_response = auth_client.login(json=login_data)

    token = login_response.access_token

    return Client(
        base_url="http://localhost:8000/api",
        timeout=50,
        headers=[
            {"Authorization": f"Bearer {token}"}
            ]
    )
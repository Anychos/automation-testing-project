from httpx import Response

from src.api.clients.auth import AuthAPIClient
from src.api.clients.base import BaseAPIClient
from src.api.clients.private_client_builder import private_client_builder
from src.api.schemas.auth import (
    LoginRequestSchema,
)
from src.api.tools.routes import Route


class UsersAPIClient(BaseAPIClient):
    def get_user_me_api(self) -> Response:
        return self.get(url=f"{Route.USERS}/me")


def get_users_client(
    auth_client: AuthAPIClient, login_data: LoginRequestSchema
) -> UsersAPIClient:
    return UsersAPIClient(
        client=private_client_builder(auth_client=auth_client, login_data=login_data)
    )

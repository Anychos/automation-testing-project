from src.api.clients import public_client_builder
from src.api.schemas.auth import LoginRequestSchema
from src.api.schemas.auth import RegisterRequestSchema
from httpx import Response
from src.api.tools.routes import Route
from api.clients.base import BaseAPIClient


class AuthAPIClient(BaseAPIClient):
    def register_api(self, json: RegisterRequestSchema) -> Response:
        return self.post(url=Route.REGISTER, json=json)

    def login_api(self, json: LoginRequestSchema) -> Response:
        return self.post(url=Route.LOGIN, json=json)


def get_auth_client() -> AuthAPIClient:
    return AuthAPIClient(client=public_client_builder())
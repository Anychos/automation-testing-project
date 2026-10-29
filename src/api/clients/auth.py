from typing import Any

from httpx import Response

from src.api.clients.base import BaseAPIClient
from src.api.clients.public_client_builder import public_client_builder
from src.api.schemas.auth import (
    LoginRequestSchema,
    LoginResponseSchema,
    RegisterRequestSchema,
    RegisterResponseSchema,
)
from src.api.tools.routes import Route


class AuthAPIClient(BaseAPIClient):
    def register_api(self, json: RegisterRequestSchema | dict[str, Any]) -> Response:
        if isinstance(json, RegisterRequestSchema):
            request_body = json.model_dump(mode="json")
        else:
            request_body = json
        return self.post(url=Route.REGISTER, json=request_body)

    def register(self, json: RegisterRequestSchema) -> RegisterResponseSchema:
        register_response = self.register_api(json=json)
        register_response.raise_for_status()
        return RegisterResponseSchema.model_validate_json(register_response.content)

    def login_api(self, json: LoginRequestSchema | dict[str, Any]) -> Response:
        if isinstance(json, LoginRequestSchema):
            request_body = json.model_dump(mode="json")
        else:
            request_body = json
        return self.post(url=Route.LOGIN, json=request_body)

    def login(self, json: LoginRequestSchema) -> LoginResponseSchema:
        login_response = self.login_api(json=json)
        login_response.raise_for_status()
        return LoginResponseSchema.model_validate_json(login_response.content)


def get_auth_client() -> AuthAPIClient:
    return AuthAPIClient(client=public_client_builder())

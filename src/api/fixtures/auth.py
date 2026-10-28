from collections.abc import Iterator

import pytest
from pydantic import BaseModel

from config import settings
from src.api.clients.auth import AuthAPIClient, get_auth_client
from src.api.schemas.auth import LoginRequestSchema, LoginResponseSchema


class AuthFixture(BaseModel):
    request: LoginRequestSchema
    response: LoginResponseSchema

    @property
    def token(self) -> str:
        return self.response.access_token


class AdminFixture(AuthFixture):
    pass


class UserFixture(AuthFixture):
    pass


@pytest.fixture
def auth_client() -> Iterator[AuthAPIClient]:

    auth_client = get_auth_client()

    yield auth_client

    auth_client.close()


@pytest.fixture(scope="function")
def admin(auth_client: AuthAPIClient) -> AdminFixture:
    login_request = LoginRequestSchema(
        email=settings.admin_data.email, password=settings.admin_data.password
    )
    login_response = auth_client.login(json=login_request)
    return AdminFixture(request=login_request, response=login_response)


@pytest.fixture(scope="function")
def user(auth_client: AuthAPIClient) -> UserFixture:
    login_request = LoginRequestSchema(
        email=settings.user_data_session.email,
        password=settings.user_data_session.password,
    )
    login_response = auth_client.login(json=login_request)
    return UserFixture(request=login_request, response=login_response)

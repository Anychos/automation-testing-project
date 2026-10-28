from collections.abc import Iterator

import pytest
from pydantic import BaseModel

from src.api.clients.auth import AuthAPIClient
from src.api.clients.users import UsersAPIClient, get_users_client
from src.api.schemas.auth import (
    LoginRequestSchema,
    RegisterRequestSchema,
    RegisterResponseSchema,
)


class UserFixture(BaseModel):
    request: RegisterRequestSchema
    response: RegisterResponseSchema


@pytest.fixture
def users_client(
    auth_client: AuthAPIClient, registered_user: UserFixture
) -> Iterator[UsersAPIClient]:
    login_data = LoginRequestSchema(
        email=registered_user.request.email,
        password=registered_user.request.password,
    )
    users_client = get_users_client(
        auth_client=auth_client,
        login_data=login_data,
    )

    try:
        yield users_client
    finally:
        users_client.close()


@pytest.fixture(scope="function")
def registered_user(auth_client: AuthAPIClient) -> UserFixture:
    register_request = RegisterRequestSchema()

    register_response = auth_client.register(json=register_request)

    return UserFixture(request=register_request, response=register_response)

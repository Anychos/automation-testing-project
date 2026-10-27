from src.api.clients.users import get_users_client
from collections.abc import Iterator
import pytest
from pydantic import BaseModel

from api.clients.auth import AuthAPIClient
from api.schemas.auth import RegisterRequestSchema, RegisterResponseSchema


class UserFixture(BaseModel):
    request: RegisterRequestSchema
    response: RegisterResponseSchema


@pytest.fixture
def users_client() -> Iterator[AuthAPIClient]:

    users_client = get_users_client()

    yield users_client

    users_client.close()


@pytest.fixture(scope="function")
def registered_user(auth_client: AuthAPIClient) -> UserFixture:
    register_request = RegisterRequestSchema()

    register_response = auth_client.register(json=register_request)

    return UserFixture(request=register_request, response=register_response)



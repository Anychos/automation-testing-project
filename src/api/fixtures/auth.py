import pytest

from api.clients.auth import AuthAPIClient, get_auth_client


@pytest.fixture
def auth_client() -> AuthAPIClient:
    return get_auth_client()

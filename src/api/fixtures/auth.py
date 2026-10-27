from collections.abc import Iterator
import pytest

from api.clients.auth import AuthAPIClient, get_auth_client


@pytest.fixture
def auth_client() -> Iterator[AuthAPIClient]:

    auth_client = get_auth_client()

    yield auth_client

    auth_client.close()

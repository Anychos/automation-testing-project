from src.api.clients.health import get_health_client
from collections.abc import Iterator
import pytest

from api.clients.health import HealthAPIClient


@pytest.fixture
def health_client() -> Iterator[HealthAPIClient]:

    users_client = get_health_client()

    yield users_client

    users_client.close()
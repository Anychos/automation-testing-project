from collections.abc import Iterator

import pytest

from src.api.clients.health import HealthAPIClient, get_health_client


@pytest.fixture
def health_client() -> Iterator[HealthAPIClient]:
    health_client = get_health_client()

    yield health_client

    health_client.close()

import pytest
from httpx import HTTPError
from pydantic import ValidationError

from config import settings
from src.api.clients.health import get_health_client
from src.api.schemas.health import HealthCheckResponseSchema
from src.api.tools.routes import Route

pytest_plugins = [
    "src.api.fixtures.auth",
    "src.api.fixtures.health",
    "src.api.fixtures.rooms",
    "src.api.fixtures.bookings",
    "src.api.fixtures.users",
]


def pytest_sessionstart(session: pytest.Session) -> None:
    if session.config.option.collectonly:
        return

    readiness_url = f"{settings.client_settings.url}{Route.HEALTH}/ready"
    health_client = get_health_client()

    try:
        ready_response = health_client.get_ready_api()
        if ready_response.status_code != 200:
            pytest.exit(
                _preflight_error(
                    readiness_url=readiness_url,
                    reason=f"received HTTP {ready_response.status_code}",
                ),
                returncode=2,
            )

        ready_response_schema = HealthCheckResponseSchema.model_validate_json(
            ready_response.content
        )
        if ready_response_schema.status != "ok":
            pytest.exit(
                _preflight_error(
                    readiness_url=readiness_url,
                    reason=(
                        "received unexpected health status "
                        f"'{ready_response_schema.status}'"
                    ),
                ),
                returncode=2,
            )
    except HTTPError as error:
        pytest.exit(
            _preflight_error(readiness_url=readiness_url, reason=str(error)),
            returncode=2,
        )
    except ValidationError as error:
        pytest.exit(
            _preflight_error(
                readiness_url=readiness_url,
                reason=f"received invalid readiness response: {error}",
            ),
            returncode=2,
        )
    finally:
        health_client.close()


def _preflight_error(*, readiness_url: str, reason: str) -> str:
    return (
        f"API preflight failed for {readiness_url}: {reason}. "
        "Check that the API is running and CLIENT_SETTINGS.BASE_URL is correct."
    )

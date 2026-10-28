from src.api.assertions.base import assert_field_value, assert_status_code
from src.api.clients.health import HealthAPIClient
from src.api.schemas.health import HealthCheckResponseSchema


class TestHealthPositive:
    def test_live_returns_200(self, health_client: HealthAPIClient) -> None:
        # Arrange

        # Act
        live_response = health_client.get_live_api()

        # Assert
        assert_status_code(expected=200, actual=live_response.status_code)
        live_response_schema = HealthCheckResponseSchema.model_validate_json(
            live_response.content
        )
        assert_field_value(
            expected="ok",
            actual=live_response_schema.status,
            field_name="status",
        )

    def test_ready_returns_200(self, health_client: HealthAPIClient) -> None:
        # Arrange

        # Act
        ready_response = health_client.get_ready_api()

        # Assert
        assert_status_code(expected=200, actual=ready_response.status_code)
        ready_response_schema = HealthCheckResponseSchema.model_validate_json(
            ready_response.content
        )
        assert_field_value(
            expected="ok",
            actual=ready_response_schema.status,
            field_name="status",
        )

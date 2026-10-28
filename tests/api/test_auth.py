from src.api.assertions.auth import assert_login_response, assert_register_response
from src.api.assertions.base import assert_status_code
from src.api.clients.auth import AuthAPIClient
from src.api.fixtures.auth import AdminFixture, UserFixture
from src.api.fixtures.users import UserFixture as RegisteredUserFixture
from src.api.schemas.auth import (
    LoginRequestSchema,
    LoginResponseSchema,
    RegisterRequestSchema,
    RegisterResponseSchema,
)


class TestAuthPositive:
    def test_register_new_user_returns_201(self, auth_client: AuthAPIClient) -> None:
        # Arrange
        register_request = RegisterRequestSchema()

        # Act
        register_response = auth_client.register_api(json=register_request)

        # Assert
        assert_status_code(expected=201, actual=register_response.status_code)
        register_response_schema = RegisterResponseSchema.model_validate_json(
            register_response.content
        )
        assert_register_response(
            register_request=register_request,
            register_response=register_response_schema,
        )

    def test_login_existing_user_returns_200(
        self, auth_client: AuthAPIClient, admin: AdminFixture
    ) -> None:
        # Arrange
        login_request = LoginRequestSchema(
            email=admin.request.email,
            password=admin.request.password,
        )

        # Act
        login_response = auth_client.login_api(json=login_request)

        # Assert
        assert_status_code(expected=200, actual=login_response.status_code)
        login_response_schema = LoginResponseSchema.model_validate_json(
            login_response.content
        )
        assert_login_response(login_response=login_response_schema)


class TestAuthNegative:
    def test_login_with_invalid_password_returns_401(
        self, auth_client: AuthAPIClient, user: UserFixture
    ) -> None:
        # Arrange
        login_request = LoginRequestSchema(
            email=user.request.email,
            password="InvalidPassword123!",
        )

        # Act
        login_response = auth_client.login_api(json=login_request)

        # Assert
        assert_status_code(expected=401, actual=login_response.status_code)

    def test_register_existing_user_returns_409(
        self,
        auth_client: AuthAPIClient,
        registered_user: RegisteredUserFixture,
    ) -> None:
        # Arrange
        register_request = registered_user.request

        # Act
        register_response = auth_client.register_api(json=register_request)

        # Assert
        assert_status_code(expected=409, actual=register_response.status_code)

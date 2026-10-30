from http import HTTPStatus
from uuid import uuid4

import pytest

from src.api.assertions.auth import assert_login_response, assert_register_response
from src.api.assertions.base import assert_status_code
from src.api.assertions.error import (
    assert_http_error_response,
    assert_validation_error_response,
)
from src.api.clients.auth import AuthAPIClient
from src.api.fixtures.auth import AdminFixture, UserFixture
from src.api.fixtures.users import UserFixture as RegisteredUserFixture
from src.api.schemas.auth import (
    LoginRequestSchema,
    LoginResponseSchema,
    RegisterRequestSchema,
    RegisterResponseSchema,
)
from src.api.schemas.error import (
    ErrorResponseSchema,
    FieldWithErrorSchema,
    ValidationErrorResponseSchema,
)


@pytest.mark.auth
@pytest.mark.positive
class TestAuthPositive:
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_register_new_user_returns_201(self, auth_client: AuthAPIClient) -> None:
        # Arrange
        register_request = RegisterRequestSchema()

        # Act
        register_response = auth_client.register_api(json=register_request)

        # Assert
        assert_status_code(
            expected=HTTPStatus.CREATED, actual=register_response.status_code
        )
        register_response_schema = RegisterResponseSchema.model_validate_json(
            register_response.content
        )
        assert_register_response(
            register_request=register_request,
            register_response=register_response_schema,
        )

    @pytest.mark.regression
    def test_register_with_mixed_case_email_returns_lowercase_email(
        self, auth_client: AuthAPIClient
    ) -> None:
        # Arrange
        register_request = RegisterRequestSchema(
            email=f"Junior{uuid4().hex}@example.com"
        )

        # Act
        register_response = auth_client.register_api(json=register_request)

        # Assert
        assert_status_code(
            expected=HTTPStatus.CREATED, actual=register_response.status_code
        )
        register_response_schema = RegisterResponseSchema.model_validate_json(
            register_response.content
        )
        assert_register_response(
            register_request=register_request,
            register_response=register_response_schema,
        )

    @pytest.mark.regression
    @pytest.mark.parametrize(
        "password",
        [
            pytest.param("p" * 8, id="minimum-length-8"),
            pytest.param("p" * 64, id="maximum-length-64"),
        ],
    )
    def test_register_with_password_boundary_returns_201(
        self, auth_client: AuthAPIClient, password: str
    ) -> None:
        # Arrange
        register_request = RegisterRequestSchema(password=password)

        # Act
        register_response = auth_client.register_api(json=register_request)

        # Assert
        assert_status_code(
            expected=HTTPStatus.CREATED, actual=register_response.status_code
        )
        register_response_schema = RegisterResponseSchema.model_validate_json(
            register_response.content
        )
        assert_register_response(
            register_request=register_request,
            register_response=register_response_schema,
        )

    @pytest.mark.smoke
    @pytest.mark.regression
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
        assert_status_code(expected=HTTPStatus.OK, actual=login_response.status_code)
        login_response_schema = LoginResponseSchema.model_validate_json(
            login_response.content
        )
        assert_login_response(login_response=login_response_schema)

    @pytest.mark.regression
    def test_registered_user_can_login_with_registered_credentials(
        self, auth_client: AuthAPIClient, registered_user: RegisteredUserFixture
    ) -> None:
        # Arrange
        login_request = LoginRequestSchema(
            email=registered_user.request.email,
            password=registered_user.request.password,
        )

        # Act
        login_response = auth_client.login_api(json=login_request)

        # Assert
        assert_status_code(expected=HTTPStatus.OK, actual=login_response.status_code)
        login_response_schema = LoginResponseSchema.model_validate_json(
            login_response.content
        )
        assert_login_response(login_response=login_response_schema)


@pytest.mark.auth
@pytest.mark.negative
class TestAuthNegative:
    @pytest.mark.regression
    @pytest.mark.parametrize(
        "email, password",
        [
            pytest.param("existing-user", "InvalidPassword123!", id="wrong-password"),
            pytest.param("existing-user", "", id="empty-password"),
            pytest.param("unknown-user", "ValidPassword123!", id="unknown-email"),
        ],
    )
    def test_login_with_invalid_credentials_returns_401(
        self,
        auth_client: AuthAPIClient,
        user: UserFixture,
        email: str,
        password: str,
    ) -> None:
        # Arrange
        if email == "existing-user":
            login_request = LoginRequestSchema(
                email=user.request.email,
                password=password,
            )
        else:
            login_request = LoginRequestSchema(
                email=RegisterRequestSchema().email,
                password=password,
            )

        # Act
        login_response = auth_client.login_api(json=login_request)

        # Assert
        assert_status_code(
            expected=HTTPStatus.UNAUTHORIZED, actual=login_response.status_code
        )
        error_response = ErrorResponseSchema.model_validate_json(login_response.content)
        assert_http_error_response(
            response=error_response,
            expected_code="UNAUTHORIZED",
            expected_message="Неверный email или пароль",
        )

    @pytest.mark.regression
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
        assert_status_code(
            expected=HTTPStatus.CONFLICT, actual=register_response.status_code
        )
        error_response = ErrorResponseSchema.model_validate_json(
            register_response.content
        )
        assert_http_error_response(
            response=error_response,
            expected_code="EMAIL_ALREADY_EXISTS",
            expected_message="Email уже зарегистрирован",
        )

    @pytest.mark.regression
    @pytest.mark.parametrize(
        "register_request, expected_fields",
        [
            pytest.param(
                {"email": "bad-email", "password": "ValidPassword123!"},
                [
                    FieldWithErrorSchema(
                        field="email",
                        message=(
                            "value is not a valid email address: An email address must have an @-sign."
                        ),
                    )
                ],
                id="invalid-email-format",
            ),
            pytest.param(
                {"email": "", "password": "ValidPassword123!"},
                [
                    FieldWithErrorSchema(
                        field="email",
                        message=(
                            "value is not a valid email address: An email address must have an @-sign."
                        ),
                    )
                ],
                id="empty-email",
            ),
            pytest.param(
                {"email": "valid@example.com", "password": "p" * 7},
                [
                    FieldWithErrorSchema(
                        field="password",
                        message="String should have at least 8 characters",
                    )
                ],
                id="password-length-7",
            ),
            pytest.param(
                {"email": "valid@example.com", "password": "p" * 65},
                [
                    FieldWithErrorSchema(
                        field="password",
                        message="String should have at most 64 characters",
                    )
                ],
                id="password-length-65",
            ),
            pytest.param(
                {"email": "valid@example.com", "password": ""},
                [
                    FieldWithErrorSchema(
                        field="password",
                        message="String should have at least 8 characters",
                    )
                ],
                id="empty-password",
            ),
            pytest.param(
                {"password": "ValidPassword123!"},
                [FieldWithErrorSchema(field="email", message="Field required")],
                id="missing-email",
            ),
            pytest.param(
                {"email": "valid@example.com"},
                [FieldWithErrorSchema(field="password", message="Field required")],
                id="missing-password",
            ),
            pytest.param(
                {"email": None, "password": "ValidPassword123!"},
                [
                    FieldWithErrorSchema(
                        field="email", message="Input should be a valid string"
                    )
                ],
                id="null-email",
            ),
            pytest.param(
                {"email": "valid@example.com", "password": None},
                [
                    FieldWithErrorSchema(
                        field="password", message="Input should be a valid string"
                    )
                ],
                id="null-password",
            ),
            pytest.param(
                {"email": 123, "password": "ValidPassword123!"},
                [
                    FieldWithErrorSchema(
                        field="email", message="Input should be a valid string"
                    )
                ],
                id="email-wrong-type",
            ),
            pytest.param(
                {"email": "valid@example.com", "password": 123},
                [
                    FieldWithErrorSchema(
                        field="password", message="Input should be a valid string"
                    )
                ],
                id="password-wrong-type",
            ),
            pytest.param(
                {
                    "email": "valid@example.com",
                    "password": "ValidPassword123!",
                    "role": "ADMIN",
                },
                [
                    FieldWithErrorSchema(
                        field="role", message="Extra inputs are not permitted"
                    )
                ],
                id="unexpected-role-field",
            ),
        ],
    )
    def test_register_with_invalid_input_returns_422(
        self,
        auth_client: AuthAPIClient,
        register_request: dict[str, object],
        expected_fields: list[FieldWithErrorSchema],
    ) -> None:
        # Arrange

        # Act
        register_response = auth_client.register_api(json=register_request)

        # Assert
        assert_status_code(
            expected=HTTPStatus.UNPROCESSABLE_ENTITY,
            actual=register_response.status_code,
        )
        error_response = ValidationErrorResponseSchema.model_validate_json(
            register_response.content
        )
        assert_validation_error_response(
            response=error_response,
            expected_code="VALIDATION_ERROR",
            expected_message="Неверные данные",
            expected_fields=expected_fields,
        )

    @pytest.mark.regression
    @pytest.mark.parametrize(
        "login_request, expected_fields",
        [
            pytest.param(
                {"email": "bad-email", "password": "ValidPassword123!"},
                [
                    FieldWithErrorSchema(
                        field="email",
                        message=(
                            "value is not a valid email address: An email address must have an @-sign."
                        ),
                    )
                ],
                id="invalid-email-format",
            ),
            pytest.param(
                {"password": "ValidPassword123!"},
                [FieldWithErrorSchema(field="email", message="Field required")],
                id="missing-email",
            ),
            pytest.param(
                {"email": "valid@example.com"},
                [FieldWithErrorSchema(field="password", message="Field required")],
                id="missing-password",
            ),
            pytest.param(
                {"email": None, "password": "ValidPassword123!"},
                [
                    FieldWithErrorSchema(
                        field="email", message="Input should be a valid string"
                    )
                ],
                id="null-email",
            ),
            pytest.param(
                {"email": "valid@example.com", "password": None},
                [
                    FieldWithErrorSchema(
                        field="password", message="Input should be a valid string"
                    )
                ],
                id="null-password",
            ),
            pytest.param(
                {"email": 123, "password": "ValidPassword123!"},
                [
                    FieldWithErrorSchema(
                        field="email", message="Input should be a valid string"
                    )
                ],
                id="email-wrong-type",
            ),
            pytest.param(
                {"email": "valid@example.com", "password": 123},
                [
                    FieldWithErrorSchema(
                        field="password", message="Input should be a valid string"
                    )
                ],
                id="password-wrong-type",
            ),
            pytest.param(
                {
                    "email": "valid@example.com",
                    "password": "ValidPassword123!",
                    "role": "ADMIN",
                },
                [
                    FieldWithErrorSchema(
                        field="role", message="Extra inputs are not permitted"
                    )
                ],
                id="unexpected-role-field",
            ),
        ],
    )
    def test_login_with_invalid_input_returns_422(
        self,
        auth_client: AuthAPIClient,
        login_request: dict[str, object],
        expected_fields: list[FieldWithErrorSchema],
    ) -> None:
        # Arrange

        # Act
        login_response = auth_client.login_api(json=login_request)

        # Assert
        assert_status_code(
            expected=HTTPStatus.UNPROCESSABLE_ENTITY,
            actual=login_response.status_code,
        )
        error_response = ValidationErrorResponseSchema.model_validate_json(
            login_response.content
        )
        assert_validation_error_response(
            response=error_response,
            expected_code="VALIDATION_ERROR",
            expected_message="Неверные данные",
            expected_fields=expected_fields,
        )

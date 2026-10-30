from src.api.assertions.base import assert_field_value
from src.api.schemas.auth import (
    LoginResponseSchema,
    RegisterRequestSchema,
    RegisterResponseSchema,
)


def assert_login_response(login_response: LoginResponseSchema) -> None:
    assert_field_value(
        expected="bearer",
        actual=login_response.token_type,
        field_name="token_type",
    )
    assert login_response.access_token, "Поле 'access_token' не должно быть пустым"


def assert_register_response(
    *,
    register_request: RegisterRequestSchema,
    register_response: RegisterResponseSchema,
) -> None:
    assert_field_value(
        expected=register_request.email.lower(),
        actual=register_response.email,
        field_name="email",
    )
    assert_field_value(
        expected="USER", actual=register_response.role, field_name="role"
    )

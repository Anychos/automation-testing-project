from src.api.schemas.auth import LoginResponseSchema
from src.api.assertions.base import assert_field_value
from api.schemas.auth import LoginRequestSchema, RegisterRequestSchema, RegisterResponseSchema


def assert_register_response(register_request: RegisterRequestSchema, register_response: RegisterResponseSchema) -> None:
    assert_field_value(expected=register_request.email, actual=register_response.email)
    assert_field_value(expected="USER", actual=register_response.role, field_name="role")
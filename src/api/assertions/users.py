from api.assertions.base import assert_field_value
from api.schemas.auth import RegisterResponseSchema
from api.schemas.users import GetUserMeResponseSchema


def assert_get_user_me_response(register_response: RegisterResponseSchema, get_user_me_response: GetUserMeResponseSchema) -> None:
    assert_field_value(expected=register_response.id, actual=get_user_me_response.id, field_name="id")
    assert_field_value(expected=register_response.email, actual=get_user_me_response.email, field_name="email")
    assert_field_value(expected=register_response.role, actual=get_user_me_response.role, field_name="role")
    assert_field_value(expected=register_response.created_at, actual=get_user_me_response.created_at, field_name="created_at")
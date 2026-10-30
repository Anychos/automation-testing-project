from src.api.assertions.base import assert_field_value
from src.api.schemas.error import (
    ErrorResponseSchema,
    ErrorSchema,
    FieldWithErrorSchema,
    ValidationErrorResponseSchema,
    ValidationErrorSchema,
)


def assert_http_error(
    *, actual_error: ErrorSchema, expected_code: str, expected_message: str
) -> None:
    assert_field_value(
        expected=expected_code, actual=actual_error.code, field_name="error.code"
    )
    assert_field_value(
        expected=expected_message,
        actual=actual_error.message,
        field_name="error.message",
    )


def assert_validation_error_field(
    *, actual_field: FieldWithErrorSchema, expected_field: str, expected_message: str
) -> None:
    assert_field_value(
        expected=expected_field, actual=actual_field.field, field_name="field"
    )
    assert_field_value(
        expected=expected_message, actual=actual_field.message, field_name="message"
    )


def assert_validation_error(
    *,
    actual_error: ValidationErrorSchema,
    expected_code: str,
    expected_message: str,
    expected_fields: list[FieldWithErrorSchema],
) -> None:
    assert_http_error(
        actual_error=actual_error,
        expected_code=expected_code,
        expected_message=expected_message,
    )
    assert_field_value(
        expected=len(expected_fields),
        actual=len(actual_error.fields),
        field_name="error.fields length",
    )

    actual_fields = sorted(
        actual_error.fields, key=lambda item: (item.field, item.message)
    )
    expected_fields_sorted = sorted(
        expected_fields, key=lambda item: (item.field, item.message)
    )
    for actual, expected in zip(actual_fields, expected_fields_sorted):
        assert_validation_error_field(
            actual_field=actual,
            expected_field=expected.field,
            expected_message=expected.message,
        )


def assert_http_error_response(
    *, response: ErrorResponseSchema, expected_code: str, expected_message: str
) -> None:
    assert_http_error(
        actual_error=response.error,
        expected_code=expected_code,
        expected_message=expected_message,
    )


def assert_validation_error_response(
    *,
    response: ValidationErrorResponseSchema,
    expected_code: str,
    expected_message: str,
    expected_fields: list[FieldWithErrorSchema],
) -> None:
    assert_validation_error(
        actual_error=response.error,
        expected_code=expected_code,
        expected_message=expected_message,
        expected_fields=expected_fields,
    )

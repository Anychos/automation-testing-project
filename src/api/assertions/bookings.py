from datetime import time
from uuid import UUID

from src.api.assertions.base import assert_field_value
from src.api.schemas.bookings import (
    BaseBookingSchema,
    CancelBookingResponseSchema,
    CreateBookingRequestSchema,
    CreateBookingResponseSchema,
    GetBookingResponseSchema,
    PayBookingResponseSchema,
)


def assert_booking(
    expected_booking_schema: BaseBookingSchema, actual_booking_schema: BaseBookingSchema
) -> None:
    assert_field_value(
        expected=expected_booking_schema.id,
        actual=actual_booking_schema.id,
        field_name="id",
    )
    assert_field_value(
        expected=expected_booking_schema.user_id,
        actual=actual_booking_schema.user_id,
        field_name="user_id",
    )
    assert_field_value(
        expected=expected_booking_schema.room_id,
        actual=actual_booking_schema.room_id,
        field_name="room_id",
    )
    assert_field_value(
        expected=expected_booking_schema.title,
        actual=actual_booking_schema.title,
        field_name="title",
    )
    assert_field_value(
        expected=expected_booking_schema.booking_date,
        actual=actual_booking_schema.booking_date,
        field_name="booking_date",
    )
    assert_field_value(
        expected=expected_booking_schema.start_time,
        actual=actual_booking_schema.start_time,
        field_name="start_time",
    )
    assert_field_value(
        expected=expected_booking_schema.end_time,
        actual=actual_booking_schema.end_time,
        field_name="end_time",
    )
    assert_field_value(
        expected=expected_booking_schema.duration_minutes,
        actual=actual_booking_schema.duration_minutes,
        field_name="duration_minutes",
    )
    assert_field_value(
        expected=expected_booking_schema.attendees,
        actual=actual_booking_schema.attendees,
        field_name="attendees",
    )
    assert_field_value(
        expected=expected_booking_schema.total_price_kopeks,
        actual=actual_booking_schema.total_price_kopeks,
        field_name="total_price",
    )
    assert_field_value(
        expected=expected_booking_schema.status,
        actual=actual_booking_schema.status,
        field_name="status",
    )
    assert_field_value(
        expected=expected_booking_schema.created_at,
        actual=actual_booking_schema.created_at,
        field_name="created_at",
    )
    assert_field_value(
        expected=expected_booking_schema.updated_at,
        actual=actual_booking_schema.updated_at,
        field_name="updated_at",
    )
    assert_field_value(
        expected=expected_booking_schema.expires_at,
        actual=actual_booking_schema.expires_at,
        field_name="expires_at",
    )


def assert_create_booking_response(
    *,
    create_booking_request: CreateBookingRequestSchema,
    create_booking_response: CreateBookingResponseSchema,
    expected_user_id: UUID,
    expected_end_time: time,
    expected_total_price_kopeks: int,
    expected_status: str,
) -> None:
    assert_field_value(
        expected=create_booking_request.room_id,
        actual=create_booking_response.room_id,
        field_name="room_id",
    )
    assert_field_value(
        expected=create_booking_request.title,
        actual=create_booking_response.title,
        field_name="title",
    )
    assert_field_value(
        expected=create_booking_request.booking_date,
        actual=create_booking_response.booking_date,
        field_name="booking_date",
    )
    assert_field_value(
        expected=create_booking_request.start_time,
        actual=create_booking_response.start_time,
        field_name="start_time",
    )
    assert_field_value(
        expected=create_booking_request.duration_minutes,
        actual=create_booking_response.duration_minutes,
        field_name="duration_minutes",
    )
    assert_field_value(
        expected=create_booking_request.attendees,
        actual=create_booking_response.attendees,
        field_name="attendees",
    )
    assert_field_value(
        expected=expected_user_id,
        actual=create_booking_response.user_id,
        field_name="user_id",
    )
    assert_field_value(
        expected=expected_end_time,
        actual=create_booking_response.end_time,
        field_name="end_time",
    )
    assert_field_value(
        expected=expected_total_price_kopeks,
        actual=create_booking_response.total_price_kopeks,
        field_name="total_price_kopeks",
    )
    assert_field_value(
        expected=expected_status,
        actual=create_booking_response.status,
        field_name="status",
    )


def assert_cancel_booking_response(
    *,
    cancel_booking_response: CancelBookingResponseSchema,
    expected_booking_id: UUID,
    expected_status: str,
) -> None:
    assert_field_value(
        expected=expected_booking_id,
        actual=cancel_booking_response.id,
        field_name="id",
    )
    assert_field_value(
        expected=expected_status,
        actual=cancel_booking_response.status,
        field_name="status",
    )


def assert_pay_booking_response(
    *,
    pay_booking_response: PayBookingResponseSchema,
    expected_booking_id: UUID,
    expected_status: str,
) -> None:
    assert_field_value(
        expected=expected_booking_id,
        actual=pay_booking_response.id,
        field_name="id",
    )
    assert_field_value(
        expected=expected_status,
        actual=pay_booking_response.status,
        field_name="status",
    )


def assert_get_booking_response(
    create_booking_response: CreateBookingResponseSchema,
    get_booking_response: GetBookingResponseSchema,
) -> None:
    assert_booking(
        expected_booking_schema=create_booking_response,
        actual_booking_schema=get_booking_response,
    )

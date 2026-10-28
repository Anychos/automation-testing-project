from uuid import uuid4

from src.api.assertions.base import assert_field_value, assert_status_code
from src.api.assertions.bookings import (
    assert_booking,
    assert_get_booking_response,
)
from src.api.clients.bookings import BookingsAPIClient
from src.api.fixtures.bookings import BookingFixture
from src.api.fixtures.rooms import RoomFixture
from src.api.schemas.bookings import (
    CreateBookingRequestSchema,
    CreateBookingResponseSchema,
    GetBookingResponseSchema,
    GetBookingsResponseSchema,
    PayBookingRequestSchema,
    PayBookingResponseSchema,
)


class TestBookingsPositive:
    def test_create_booking_returns_201(
        self,
        bookings_client: BookingsAPIClient,
        created_room: RoomFixture,
    ) -> None:
        # Arrange
        create_booking_request = CreateBookingRequestSchema(room_id=created_room.id)

        # Act
        create_booking_response = bookings_client.create_booking_api(
            json=create_booking_request
        )

        # Assert
        assert_status_code(expected=201, actual=create_booking_response.status_code)
        create_booking_response_schema = (
            CreateBookingResponseSchema.model_validate_json(
                create_booking_response.content
            )
        )
        expected_end_minutes = (
            create_booking_request.start_time.hour * 60
            + create_booking_request.start_time.minute
            + create_booking_request.duration_minutes
        )
        expected_end_time = create_booking_request.start_time.replace(
            hour=expected_end_minutes // 60,
            minute=expected_end_minutes % 60,
        )
        expected_total_price = (
            created_room.response.price_per_30min_kopeks
            * create_booking_request.duration_minutes
            // 30
        )
        assert_field_value(
            expected=create_booking_request.room_id,
            actual=create_booking_response_schema.room_id,
            field_name="room_id",
        )
        assert_field_value(
            expected=create_booking_request.title,
            actual=create_booking_response_schema.title,
            field_name="title",
        )
        assert_field_value(
            expected=create_booking_request.booking_date,
            actual=create_booking_response_schema.booking_date,
            field_name="booking_date",
        )
        assert_field_value(
            expected=expected_end_time,
            actual=create_booking_response_schema.end_time,
            field_name="end_time",
        )
        assert_field_value(
            expected=expected_total_price,
            actual=create_booking_response_schema.total_price_kopeks,
            field_name="total_price_kopeks",
        )
        assert_field_value(
            expected="CREATED",
            actual=create_booking_response_schema.status,
            field_name="status",
        )

    def test_get_bookings_returns_created_booking(
        self,
        bookings_client: BookingsAPIClient,
        created_booking: BookingFixture,
    ) -> None:
        # Arrange
        booking_id = created_booking.response.id

        # Act
        bookings_response = bookings_client.get_bookings_api()

        # Assert
        assert_status_code(expected=200, actual=bookings_response.status_code)
        bookings_response_schema = GetBookingsResponseSchema.model_validate_json(
            bookings_response.content
        )
        actual_booking = next(
            booking
            for booking in bookings_response_schema.root
            if booking.id == booking_id
        )
        assert_booking(
            expected_booking_schema=created_booking.response,
            actual_booking_schema=actual_booking,
        )

    def test_get_existing_booking_returns_200(
        self,
        bookings_client: BookingsAPIClient,
        created_booking: BookingFixture,
    ) -> None:
        # Arrange
        booking_id = created_booking.response.id

        # Act
        get_booking_response = bookings_client.get_booking_api(booking_id=booking_id)

        # Assert
        assert_status_code(expected=200, actual=get_booking_response.status_code)
        get_booking_response_schema = GetBookingResponseSchema.model_validate_json(
            get_booking_response.content
        )
        assert_get_booking_response(
            create_booking_response=created_booking.response,
            get_booking_response=get_booking_response_schema,
        )

    def test_cancel_existing_booking_returns_200(
        self,
        bookings_client: BookingsAPIClient,
        created_booking: BookingFixture,
    ) -> None:
        # Arrange
        booking_id = created_booking.response.id

        # Act
        cancel_booking_response = bookings_client.cancel_booking_api(
            booking_id=booking_id
        )

        # Assert
        assert_status_code(expected=200, actual=cancel_booking_response.status_code)
        cancel_booking_response_schema = GetBookingResponseSchema.model_validate_json(
            cancel_booking_response.content
        )
        assert_field_value(
            expected=booking_id,
            actual=cancel_booking_response_schema.id,
            field_name="id",
        )
        assert_field_value(
            expected="CANCELLED",
            actual=cancel_booking_response_schema.status,
            field_name="status",
        )

    def test_pay_existing_booking_returns_202(
        self,
        bookings_client: BookingsAPIClient,
        created_booking: BookingFixture,
    ) -> None:
        # Arrange
        booking_id = created_booking.response.id
        pay_booking_request = PayBookingRequestSchema(test_scenario="success")

        # Act
        pay_booking_response = bookings_client.pay_booking_api(
            booking_id=booking_id,
            json=pay_booking_request,
        )

        # Assert
        assert_status_code(expected=202, actual=pay_booking_response.status_code)
        pay_booking_response_schema = PayBookingResponseSchema.model_validate_json(
            pay_booking_response.content
        )
        assert_field_value(
            expected=booking_id,
            actual=pay_booking_response_schema.id,
            field_name="id",
        )
        assert pay_booking_response_schema.status, (
            "Статус бронирования не должен быть пустым"
        )


class TestBookingsNegative:
    def test_create_booking_for_unknown_room_returns_404(
        self, bookings_client: BookingsAPIClient
    ) -> None:
        # Arrange
        create_booking_request = CreateBookingRequestSchema(room_id=uuid4())

        # Act
        create_booking_response = bookings_client.create_booking_api(
            json=create_booking_request
        )

        # Assert
        assert_status_code(expected=404, actual=create_booking_response.status_code)

    def test_get_unknown_booking_returns_404(
        self, bookings_client: BookingsAPIClient
    ) -> None:
        # Arrange
        unknown_booking_id = uuid4()

        # Act
        get_booking_response = bookings_client.get_booking_api(
            booking_id=unknown_booking_id
        )

        # Assert
        assert_status_code(expected=404, actual=get_booking_response.status_code)

    def test_cancel_unknown_booking_returns_404(
        self, bookings_client: BookingsAPIClient
    ) -> None:
        # Arrange
        unknown_booking_id = uuid4()

        # Act
        cancel_booking_response = bookings_client.cancel_booking_api(
            booking_id=unknown_booking_id
        )

        # Assert
        assert_status_code(expected=404, actual=cancel_booking_response.status_code)

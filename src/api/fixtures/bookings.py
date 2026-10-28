from collections.abc import Iterator

import pytest
from pydantic import BaseModel

from src.api.clients.auth import AuthAPIClient
from src.api.clients.bookings import BookingsAPIClient, get_bookings_client
from src.api.fixtures.auth import UserFixture
from src.api.fixtures.rooms import RoomFixture
from src.api.schemas.bookings import (
    CreateBookingRequestSchema,
    CreateBookingResponseSchema,
)


class BookingFixture(BaseModel):
    request: CreateBookingRequestSchema
    response: CreateBookingResponseSchema


@pytest.fixture
def bookings_client(
    auth_client: AuthAPIClient, user: UserFixture
) -> Iterator[BookingsAPIClient]:
    bookings_client = get_bookings_client(
        auth_client=auth_client,
        login_data=user.request,
    )

    try:
        yield bookings_client
    finally:
        bookings_client.close()


@pytest.fixture(scope="function")
def created_booking(
    bookings_client: BookingsAPIClient, created_room: RoomFixture
) -> BookingFixture:
    create_booking_request = CreateBookingRequestSchema(
        room_id=created_room.id,
    )

    create_booking_response = bookings_client.create_booking(
        json=create_booking_request
    )

    return BookingFixture(
        request=create_booking_request, response=create_booking_response
    )

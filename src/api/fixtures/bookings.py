from pydantic import BaseModel
from api.fixtures.rooms import RoomFixture
from api.schemas.bookings import CreateBookingRequestSchema, CreateBookingResponseSchema
from src.api.clients.bookings import get_bookings_client
from collections.abc import Iterator
import pytest

from api.clients.bookings import BookingsAPIClient


class BookingFixture(BaseModel):
    request: CreateBookingRequestSchema
    response: CreateBookingResponseSchema


@pytest.fixture
def bookings_client() -> Iterator[BookingsAPIClient]:

    users_client = get_bookings_client()

    yield users_client

    users_client.close()


@pytest.fixture(scope="function")
def created_booking(bookings_client: BookingsAPIClient, created_room: RoomFixture) -> BookingFixture:
    create_booking_request = CreateBookingRequestSchema(
        room_id=created_room.id,
    )

    create_booking_response = bookings_client.create_booking(json=create_booking_request)

    return BookingFixture(request=create_booking_request, response=create_booking_response)
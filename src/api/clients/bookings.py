from api.schemas.bookings import CreateBookingRequestSchema
from src.api.schemas.rooms import UpdateRoomRequestSchema
from src.api.schemas.rooms import CreateRoomRequestSchema
from api.clients.auth import AuthAPIClient
from src.api.clients.private_client_builder import private_client_builder
from src.api.clients import public_client_builder
from src.api.schemas.auth import LoginRequestSchema, LoginResponseSchema
from src.api.schemas.auth import RegisterRequestSchema
from httpx import Response
from src.api.tools.routes import Route
from api.clients.base import BaseAPIClient


class BookingsAPIClient(BaseAPIClient):
    def get_booking_api(self, booking_id: int) -> Response:
        return self.get(url=f"{Route.ROOMS}/{booking_id}")

    def create_booking_api(self, json: CreateBookingRequestSchema) -> Response:
        return self.post(url=Route.BOOKINGS, json=json.model_dump())

    def get_bookings_api(self) -> Response:
        return self.get(url=Route.BOOKINGS)

    def cancel_booking_api(self, booking_id: int) -> Response:
        return self.post(url=f"{Route.BOOKINGS}/{booking_id}/cancel")

    def pay_booking_api(self, booking_id: int) -> Response:
        return self.post(url=f"{Route.BOOKINGS}/{booking_id}/pay")


def get_bookings_client(auth_client: AuthAPIClient, login_data: LoginRequestSchema) -> BookingsAPIClient:
    return BookingsAPIClient(client=private_client_builder(auth_client=auth_client, login_data=login_data))
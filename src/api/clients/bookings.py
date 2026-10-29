from typing import Any
from uuid import UUID

from httpx import Response

from src.api.clients.auth import AuthAPIClient
from src.api.clients.base import BaseAPIClient
from src.api.clients.private_client_builder import private_client_builder
from src.api.schemas.auth import (
    LoginRequestSchema,
)
from src.api.schemas.bookings import (
    CreateBookingRequestSchema,
    CreateBookingResponseSchema,
    PayBookingRequestSchema,
)
from src.api.tools.routes import Route


class BookingsAPIClient(BaseAPIClient):
    def get_booking_api(self, booking_id: UUID) -> Response:
        return self.get(url=f"{Route.BOOKINGS}/{booking_id}")

    def create_booking_api(
        self, json: CreateBookingRequestSchema | dict[str, Any]
    ) -> Response:
        if isinstance(json, CreateBookingRequestSchema):
            request_body = json.model_dump(mode="json")
        else:
            request_body = json
        return self.post(url=Route.BOOKINGS, json=request_body)

    def create_booking(
        self, json: CreateBookingRequestSchema
    ) -> CreateBookingResponseSchema:
        create_booking_response = self.create_booking_api(json=json)
        create_booking_response.raise_for_status()
        return CreateBookingResponseSchema.model_validate_json(
            create_booking_response.content
        )

    def get_bookings_api(self) -> Response:
        return self.get(url=Route.BOOKINGS)

    def cancel_booking_api(self, booking_id: UUID) -> Response:
        return self.post(url=f"{Route.BOOKINGS}/{booking_id}/cancel")

    def pay_booking_api(
        self,
        booking_id: UUID,
        json: PayBookingRequestSchema | dict[str, Any] | None = None,
    ) -> Response:
        if isinstance(json, PayBookingRequestSchema):
            request_body = json.model_dump(mode="json")
        else:
            request_body = json
        return self.post(
            url=f"{Route.BOOKINGS}/{booking_id}/pay",
            json=request_body,
        )


def get_bookings_client(
    auth_client: AuthAPIClient, login_data: LoginRequestSchema
) -> BookingsAPIClient:
    return BookingsAPIClient(
        client=private_client_builder(auth_client=auth_client, login_data=login_data)
    )

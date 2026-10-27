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


class HealthAPIClient(BaseAPIClient):
    def get_live_api(self) -> Response:
        return self.get(url=f"{Route.HEALTH}/live")

    def get_ready_api(self) -> Response:
        return self.get(url=f"{Route.HEALTH}/ready")


def get_health_client() -> HealthAPIClient:
    return HealthAPIClient(client=public_client_builder())
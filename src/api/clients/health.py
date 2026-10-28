from httpx import Response

from src.api.clients.base import BaseAPIClient
from src.api.clients.public_client_builder import public_client_builder
from src.api.tools.routes import Route


class HealthAPIClient(BaseAPIClient):
    def get_live_api(self) -> Response:
        return self.get(url=f"{Route.HEALTH}/live")

    def get_ready_api(self) -> Response:
        return self.get(url=f"{Route.HEALTH}/ready")


def get_health_client() -> HealthAPIClient:
    return HealthAPIClient(client=public_client_builder())

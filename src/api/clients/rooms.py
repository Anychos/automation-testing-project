from src.api.schemas.rooms import CreateRoomResponseSchema, UpdateRoomRequestSchema
from src.api.schemas.rooms import CreateRoomRequestSchema
from api.clients.auth import AuthAPIClient
from src.api.clients.private_client_builder import private_client_builder
from src.api.clients import public_client_builder
from src.api.schemas.auth import LoginRequestSchema, LoginResponseSchema
from src.api.schemas.auth import RegisterRequestSchema
from httpx import Response
from src.api.tools.routes import Route
from api.clients.base import BaseAPIClient


class RoomsAPIClient(BaseAPIClient):
    def get_room_api(self, room_id: int) -> Response:
        return self.get(url=f"{Route.ROOMS}/{room_id}")

    def create_room_api(self, json: CreateRoomRequestSchema) -> Response:
        return self.post(url=Route.ROOMS, json=json.model_dump())

    def create_room(self, json: CreateRoomRequestSchema) -> CreateRoomResponseSchema:
        create_room_response = CreateRoomRequestSchema()
        return CreateRoomResponseSchema.model_validate_json(create_room_response.content)

    def get_rooms_api(self, *, include_inactive: bool = False) -> Response:
        params = {"include_inactive": include_inactive}
        return self.get(url=Route.ROOMS, params=params)

    def update_room_api(self, room_id: int, json: UpdateRoomRequestSchema) -> Response:
        return self.patch(url=f"{Route.ROOMS}/{room_id}", json=json.model_dump(exclude_unset=True))

    def delete_room_api(self, room_id: int) -> Response:
        return self.delete(url=f"{Route.ROOMS}/{room_id}")


def get_rooms_client(auth_client: AuthAPIClient, login_data: LoginRequestSchema) -> RoomsAPIClient:
    return RoomsAPIClient(client=private_client_builder(auth_client=auth_client, login_data=login_data))
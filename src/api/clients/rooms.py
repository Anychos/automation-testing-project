from typing import Any
from uuid import UUID

from httpx import Response

from src.api.clients.auth import AuthAPIClient
from src.api.clients.base import BaseAPIClient
from src.api.clients.private_client_builder import private_client_builder
from src.api.schemas.auth import (
    LoginRequestSchema,
)
from src.api.schemas.rooms import (
    CreateRoomRequestSchema,
    CreateRoomResponseSchema,
    UpdateRoomRequestSchema,
)
from src.api.tools.routes import Route


class RoomsAPIClient(BaseAPIClient):
    def get_room_api(self, room_id: UUID) -> Response:
        return self.get(url=f"{Route.ROOMS}/{room_id}")

    def create_room_api(
        self, json: CreateRoomRequestSchema | dict[str, Any]
    ) -> Response:
        if isinstance(json, CreateRoomRequestSchema):
            request_body = json.model_dump(mode="json")
        else:
            request_body = json
        return self.post(url=Route.ROOMS, json=request_body)

    def create_room(self, json: CreateRoomRequestSchema) -> CreateRoomResponseSchema:
        create_room_response = self.create_room_api(json=json)
        create_room_response.raise_for_status()
        return CreateRoomResponseSchema.model_validate_json(
            create_room_response.content
        )

    def get_rooms_api(self, *, include_inactive: bool = False) -> Response:
        params = {"include_inactive": include_inactive}
        return self.get(url=Route.ROOMS, params=params)

    def update_room_api(
        self, room_id: UUID, json: UpdateRoomRequestSchema | dict[str, Any]
    ) -> Response:
        if isinstance(json, UpdateRoomRequestSchema):
            request_body = json.model_dump(exclude_unset=True, mode="json")
        else:
            request_body = json
        return self.patch(
            url=f"{Route.ROOMS}/{room_id}",
            json=request_body,
        )

    def delete_room_api(self, room_id: UUID) -> Response:
        return self.delete(url=f"{Route.ROOMS}/{room_id}")


def get_rooms_client(
    auth_client: AuthAPIClient, login_data: LoginRequestSchema
) -> RoomsAPIClient:
    return RoomsAPIClient(
        client=private_client_builder(auth_client=auth_client, login_data=login_data)
    )

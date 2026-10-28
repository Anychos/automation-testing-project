from collections.abc import Iterator
from uuid import UUID

import pytest
from pydantic import BaseModel

from src.api.clients.auth import AuthAPIClient
from src.api.clients.rooms import RoomsAPIClient, get_rooms_client
from src.api.fixtures.auth import AdminFixture
from src.api.schemas.rooms import CreateRoomRequestSchema, CreateRoomResponseSchema


class RoomFixture(BaseModel):
    request: CreateRoomRequestSchema
    response: CreateRoomResponseSchema

    @property
    def id(self) -> UUID:
        return self.response.id


@pytest.fixture
def rooms_client(
    auth_client: AuthAPIClient, admin: AdminFixture
) -> Iterator[RoomsAPIClient]:
    rooms_client = get_rooms_client(
        auth_client=auth_client,
        login_data=admin.request,
    )

    try:
        yield rooms_client
    finally:
        rooms_client.close()


@pytest.fixture(scope="function")
def created_room(rooms_client: RoomsAPIClient) -> RoomFixture:
    create_room_request = CreateRoomRequestSchema()

    create_room_response = rooms_client.create_room(json=create_room_request)

    return RoomFixture(request=create_room_request, response=create_room_response)

from uuid import UUID
from src.api.clients.auth import AuthAPIClient
from pydantic import BaseModel
from api.schemas.rooms import CreateRoomRequestSchema, CreateRoomResponseSchema
from src.api.clients.rooms import get_rooms_client
from collections.abc import Iterator
import pytest

from api.clients.rooms import RoomsAPIClient


class RoomFixture(BaseModel):
    request: CreateRoomRequestSchema
    response: CreateRoomResponseSchema

    @property
    def id(self) -> UUID:
        return self.response.id


@pytest.fixture
def rooms_client() -> Iterator[RoomsAPIClient]:

    users_client = get_rooms_client()

    yield users_client

    users_client.close()


@pytest.fixture(scope="function")
def created_room(rooms_client: RoomsAPIClient) -> RoomFixture:
    create_room_request = CreateRoomRequestSchema()

    create_room_response = rooms_client.create_room(json=create_room_request)

    return RoomFixture(request=create_room_request, response=create_room_response)

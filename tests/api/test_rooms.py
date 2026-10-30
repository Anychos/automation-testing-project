from http import HTTPStatus
from uuid import uuid4

import pytest

from src.api.assertions.base import assert_field_value, assert_status_code
from src.api.assertions.rooms import (
    assert_create_room_response,
    assert_get_room_response,
    assert_room,
    assert_update_room_response,
)
from src.api.clients.auth import AuthAPIClient
from src.api.clients.rooms import RoomsAPIClient, get_rooms_client
from src.api.fixtures.auth import UserFixture
from src.api.fixtures.rooms import RoomFixture
from src.api.schemas.rooms import (
    CreateRoomRequestSchema,
    CreateRoomResponseSchema,
    GetRoomResponseSchema,
    GetRoomsResponseSchema,
    UpdateRoomRequestSchema,
    UpdateRoomResponseSchema,
)


@pytest.mark.rooms
@pytest.mark.positive
class TestRoomsPositive:
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_create_room_returns_201(self, rooms_client: RoomsAPIClient) -> None:
        # Arrange
        create_room_request = CreateRoomRequestSchema()

        # Act
        create_room_response = rooms_client.create_room_api(json=create_room_request)

        # Assert
        assert_status_code(
            expected=HTTPStatus.CREATED, actual=create_room_response.status_code
        )
        create_room_response_schema = CreateRoomResponseSchema.model_validate_json(
            create_room_response.content
        )
        assert_create_room_response(
            create_room_request=create_room_request,
            create_room_response=create_room_response_schema,
        )

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_get_rooms_returns_created_room(
        self, rooms_client: RoomsAPIClient, created_room: RoomFixture
    ) -> None:
        # Arrange
        room_id = created_room.id

        # Act
        rooms_response = rooms_client.get_rooms_api()

        # Assert
        assert_status_code(expected=HTTPStatus.OK, actual=rooms_response.status_code)
        rooms_response_schema = GetRoomsResponseSchema.model_validate_json(
            rooms_response.content
        )
        actual_room = next(
            room for room in rooms_response_schema.root if room.id == room_id
        )
        assert_room(
            actual_room_schema=actual_room,
            expected_room_schema=created_room.response,
        )

    @pytest.mark.regression
    def test_get_existing_room_returns_200(
        self, rooms_client: RoomsAPIClient, created_room: RoomFixture
    ) -> None:
        # Arrange
        room_id = created_room.id

        # Act
        get_room_response = rooms_client.get_room_api(room_id=room_id)

        # Assert
        assert_status_code(expected=HTTPStatus.OK, actual=get_room_response.status_code)
        get_room_response_schema = GetRoomResponseSchema.model_validate_json(
            get_room_response.content
        )
        assert_get_room_response(
            create_room_response=created_room.response,
            get_room_response=get_room_response_schema,
        )

    @pytest.mark.regression
    def test_update_existing_room_returns_200(
        self, rooms_client: RoomsAPIClient, created_room: RoomFixture
    ) -> None:
        # Arrange
        update_room_request = UpdateRoomRequestSchema(
            name=f"Обновленная комната {uuid4().hex[:8]}",
            capacity=5,
            price_per_30min_kopeks=50000,
            is_active=True,
        )

        # Act
        update_room_response = rooms_client.update_room_api(
            room_id=created_room.id,
            json=update_room_request,
        )

        # Assert
        assert_status_code(
            expected=HTTPStatus.OK, actual=update_room_response.status_code
        )
        update_room_response_schema = UpdateRoomResponseSchema.model_validate_json(
            update_room_response.content
        )
        assert_update_room_response(
            room_before_update=created_room.response,
            update_room_request=update_room_request,
            update_room_response=update_room_response_schema,
        )

    @pytest.mark.regression
    def test_delete_existing_room_returns_204(
        self, rooms_client: RoomsAPIClient, created_room: RoomFixture
    ) -> None:
        # Arrange
        room_id = created_room.id

        # Act
        delete_room_response = rooms_client.delete_room_api(room_id=room_id)

        # Assert
        assert_status_code(
            expected=HTTPStatus.NO_CONTENT, actual=delete_room_response.status_code
        )
        assert_field_value(
            expected=b"", actual=delete_room_response.content, field_name="body"
        )


@pytest.mark.rooms
@pytest.mark.negative
class TestRoomsNegative:
    @pytest.mark.regression
    def test_user_cannot_create_room_returns_403(
        self, auth_client: AuthAPIClient, user: UserFixture
    ) -> None:
        # Arrange
        user_rooms_client = get_rooms_client(
            auth_client=auth_client,
            login_data=user.request,
        )
        create_room_request = CreateRoomRequestSchema()

        try:
            # Act
            create_room_response = user_rooms_client.create_room_api(
                json=create_room_request
            )
        finally:
            user_rooms_client.close()

        # Assert
        assert_status_code(
            expected=HTTPStatus.FORBIDDEN, actual=create_room_response.status_code
        )

    @pytest.mark.regression
    def test_get_unknown_room_returns_404(self, rooms_client: RoomsAPIClient) -> None:
        # Arrange
        unknown_room_id = uuid4()

        # Act
        get_room_response = rooms_client.get_room_api(room_id=unknown_room_id)

        # Assert
        assert_status_code(
            expected=HTTPStatus.NOT_FOUND, actual=get_room_response.status_code
        )

    @pytest.mark.regression
    def test_delete_unknown_room_returns_404(
        self, rooms_client: RoomsAPIClient
    ) -> None:
        # Arrange
        unknown_room_id = uuid4()

        # Act
        delete_room_response = rooms_client.delete_room_api(room_id=unknown_room_id)

        # Assert
        assert_status_code(
            expected=HTTPStatus.NOT_FOUND, actual=delete_room_response.status_code
        )

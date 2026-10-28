from src.api.assertions.base import assert_field_value
from src.api.schemas.rooms import (
    BaseRoomSchema,
    CreateRoomRequestSchema,
    CreateRoomResponseSchema,
    GetRoomResponseSchema,
    UpdateRoomRequestSchema,
    UpdateRoomResponseSchema,
)


def assert_room(
    *, actual_room_schema: BaseRoomSchema, expected_room_schema: BaseRoomSchema
):
    assert_field_value(
        expected=expected_room_schema.name,
        actual=actual_room_schema.name,
        field_name="name",
    )
    assert_field_value(
        expected=expected_room_schema.capacity,
        actual=actual_room_schema.capacity,
        field_name="capacity",
    )
    assert_field_value(
        expected=expected_room_schema.price_per_30min_kopeks,
        actual=actual_room_schema.price_per_30min_kopeks,
        field_name="price_per_30min",
    )
    assert_field_value(
        expected=expected_room_schema.is_active,
        actual=actual_room_schema.is_active,
        field_name="is_active",
    )


def assert_create_room_response(
    *,
    create_room_request: CreateRoomRequestSchema,
    create_room_response: CreateRoomResponseSchema,
) -> None:
    assert_room(
        actual_room_schema=create_room_response,
        expected_room_schema=create_room_request,
    )


def assert_get_room_response(
    *,
    create_room_response: CreateRoomResponseSchema,
    get_room_response: GetRoomResponseSchema,
) -> None:
    assert_field_value(
        expected=create_room_response.id,
        actual=get_room_response.id,
        field_name="id",
    )
    assert_room(
        actual_room_schema=get_room_response, expected_room_schema=create_room_response
    )


def assert_update_room_response(
    *,
    room_before_update: BaseRoomSchema,
    update_room_request: UpdateRoomRequestSchema,
    update_room_response: UpdateRoomResponseSchema,
) -> None:
    assert_field_value(
        expected=room_before_update.id,
        actual=update_room_response.id,
        field_name="id",
    )

    requested_fields = update_room_request.model_dump(exclude_unset=True)
    for field_name, expected_value in requested_fields.items():
        assert_field_value(
            expected=expected_value,
            actual=getattr(update_room_response, field_name),
            field_name=field_name,
        )

    for field_name in (
        "name",
        "capacity",
        "price_per_30min_kopeks",
        "is_active",
    ):
        if field_name not in requested_fields:
            assert_field_value(
                expected=getattr(room_before_update, field_name),
                actual=getattr(update_room_response, field_name),
                field_name=field_name,
            )

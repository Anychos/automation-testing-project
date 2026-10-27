from uuid import UUID
from pydantic import ConfigDict, RootModel
from src.api.tools.data_generator import fake
from pydantic import BaseModel, Field


class BaseRoomSchema(BaseModel):
    id: UUID
    name: str
    capacity: int
    price_per_30min_kopeks: int
    is_active: bool


class CreateRoomRequestSchema(BaseModel):
    model_config = ConfigDict(validate_default=True, extra="forbid")

    name: str = Field(default_factory=fake.room_name, min_length=3, max_length=50)
    capacity: int = Field(default_factory=fake.room_capacity, ge=2, le=10)
    price_per_30min_kopeks: int = Field(default_factory=fake.room_price, ge=10000, le=200000)
    is_active: bool = True


class CreateRoomResponseSchema(BaseRoomSchema):
    pass


class GetRoomsResponseSchema(RootModel[list[BaseRoomSchema]]):
    pass


class GetRoomResponseSchema(BaseRoomSchema):
    pass


class UpdateRoomRequestSchema(BaseModel):
    name: str | None = Field(default=None, min_length=3, max_length=50)
    capacity: int | None = Field(default=None, ge=2, le=10)
    price_per_30min_kopeks: int | None = Field(default=None, ge=10000, le=200000)
    is_active: bool | None = None


class UpdateRoomResponseSchema(BaseRoomSchema):
    pass
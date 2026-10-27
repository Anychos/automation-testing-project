from pydantic import ConfigDict
from datetime import date, time, datetime
from enum import IntEnum
from typing import Literal
from src.api.tools.data_generator import fake
from uuid import UUID
from pydantic import BaseModel, Field, RootModel


class BaseBookingSchema(BaseModel):
    id: UUID
    user_id: UUID
    room_id: UUID
    title: str
    booking_date: date
    start_time: time
    end_time: time
    duration_minutes: Literal[30, 60, 90, 120]
    attendees: int
    total_price_kopeks: int
    status: str
    created_at: datetime
    updated_at: datetime
    expires_at: datetime


class CreateBookingRequestSchema(BaseModel):
    model_config = ConfigDict(
        validate_default=True,
        extra="forbid",
    )

    room_id: UUID

    title: str = Field(
        default_factory=fake.booking_name,
        min_length=3,
        max_length=60,
    )

    booking_date: date = Field(
        default_factory=fake.booking_date,
    )

    duration_minutes: Literal[30, 60, 90, 120] = Field(
        default_factory=fake.booking_duration,
    )

    start_time: time = Field(
        default_factory=lambda data: fake.booking_start_time(
            duration_minutes=data["duration_minutes"],
        ),
    )

    attendees: int = Field(default=1, ge=1)


class CreateBookingResponseSchema(BaseBookingSchema):
    pass


class GetBookingsResponseSchema(RootModel[list[BaseBookingSchema]]):
    pass


class GetBookingResponseSchema(BaseBookingSchema):
    pass


class CancelBookingResponseSchema(BaseBookingSchema):
    pass


class PayBookingRequestSchema(BaseBookingSchema):
    test_scenario: Literal["success", "failure", "no_response"]


class PayBookingResponseSchema(BaseBookingSchema):
    pass
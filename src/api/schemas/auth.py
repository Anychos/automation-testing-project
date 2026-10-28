from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from src.api.tools.data_generator import fake


class RegisterRequestSchema(BaseModel):
    model_config = ConfigDict(validate_default=True, extra="forbid")

    email: EmailStr = Field(default_factory=fake.email)
    password: str = Field(min_length=8, max_length=64, default_factory=fake.password)


class LoginRequestSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")

    email: EmailStr
    password: str


class RegisterResponseSchema(BaseModel):
    id: UUID
    email: EmailStr
    role: Literal["USER", "ADMIN"]
    created_at: datetime


class LoginResponseSchema(BaseModel):
    access_token: str = Field(min_length=1)
    token_type: Literal["bearer"] = "bearer"

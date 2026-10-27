from datetime import datetime
from typing import Literal
from uuid import UUID
from pydantic import BaseModel, EmailStr


class GetUserMeResponseSchema(BaseModel):
    id: UUID
    email: EmailStr
    role: Literal["USER", "ADMIN"]
    created_at: datetime

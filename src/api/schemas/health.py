from pydantic import BaseModel


class HealthCheckResponseSchema(BaseModel):
    status: str 
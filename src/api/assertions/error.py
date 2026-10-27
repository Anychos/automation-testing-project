from pydantic import Field
from pydantic import BaseModel


class ErrorSchema(BaseModel):
    code: str
    message: str


class FieldWithErrorSchema(BaseModel):
    field: str
    message: str


class ValidationErrorSchema(ErrorSchema):
    fields: list[FieldWithErrorSchema] = Field(min_length=1)


class ErrorResponseSchema(BaseModel):
    error: ErrorSchema


class ValidationErrorResponseSchema(BaseModel):
    error: ValidationErrorSchema
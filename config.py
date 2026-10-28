from pydantic import BaseModel, EmailStr, Field, HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class ClientSettings(BaseModel):
    base_url: HttpUrl
    timeout: float = Field(gt=0)

    @property
    def url(self) -> str:
        return str(self.base_url)


class UserDataSession(BaseModel):
    email: EmailStr
    password: str


class AdminData(BaseModel):
    email: EmailStr
    password: str


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_nested_delimiter=".",
        extra="ignore",
    )

    client_settings: ClientSettings
    admin_data: AdminData
    user_data_session: UserDataSession


settings = Settings()

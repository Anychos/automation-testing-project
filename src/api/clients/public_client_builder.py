from httpx import Client

from config import settings


def public_client_builder() -> Client:
    return Client(
        base_url=settings.client_settings.url, timeout=settings.client_settings.timeout
    )

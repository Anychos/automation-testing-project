from httpx import Client


def public_client_builder() -> Client:
    return Client(
        base_url="http://localhost:8000/api",
        timeout=50
    )
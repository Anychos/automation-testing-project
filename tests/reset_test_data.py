"""Reset local API test data with the ADMIN account from the project .env.

Run from any working directory with:
    python tests/reset_test_data.py
"""

import os
import sys
from pathlib import Path

import httpx

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

RESET_PATH = "/api/test-data/reset"
RESET_CONFIRMATION = "reset-test-data"


def main() -> int:
    # config.py reads .env relative to the current working directory.
    os.chdir(PROJECT_ROOT)

    from config import settings
    from src.api.clients.auth import get_auth_client
    from src.api.schemas.auth import LoginRequestSchema

    print(
        "WARNING: this resets API test data and invalidates all tokens. "
        "Run after tests and payment processing; Kafka and payment-service "
        "data are not reset."
    )

    auth_client = get_auth_client()
    try:
        login_response = auth_client.login(
            json=LoginRequestSchema(
                email=settings.admin_data.email,
                password=settings.admin_data.password,
            )
        )
    except httpx.HTTPError as error:
        print(f"ADMIN login failed: {error}", file=sys.stderr)
        return 1
    finally:
        auth_client.close()

    try:
        api_base_url = httpx.URL(settings.client_settings.url)
        reset_url = api_base_url.copy_with(
            path=RESET_PATH,
            query=None,
            fragment=None,
        )
        with httpx.Client(
            timeout=settings.client_settings.timeout,
            headers={"Authorization": f"Bearer {login_response.access_token}"},
        ) as client:
            response = client.post(
                reset_url,
                json={"confirm": RESET_CONFIRMATION},
            )
    except httpx.HTTPError as error:
        print(f"Test data reset request failed: {error}", file=sys.stderr)
        return 1

    if response.status_code != 204:
        details = response.text.strip()
        message = f"Test data reset failed: HTTP {response.status_code}"
        if details:
            message += f"\n{details}"
        print(message, file=sys.stderr)
        return 1

    print("Test data reset completed successfully (HTTP 204).")
    print("All previous tokens are invalid. Log in again before running tests.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

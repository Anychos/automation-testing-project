from http import HTTPStatus

import pytest

from src.api.assertions.base import assert_status_code
from src.api.assertions.users import assert_get_user_me_response
from src.api.clients.auth import AuthAPIClient
from src.api.clients.users import UsersAPIClient
from src.api.fixtures.users import UserFixture
from src.api.schemas.users import GetUserMeResponseSchema
from src.api.tools.routes import Route


@pytest.mark.users
@pytest.mark.positive
class TestUsersPositive:
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_get_current_user_returns_200(
        self,
        users_client: UsersAPIClient,
        registered_user: UserFixture,
    ) -> None:
        # Arrange
        # The users_client is authorized as the registered_user fixture.

        # Act
        get_user_me_response = users_client.get_user_me_api()

        # Assert
        assert_status_code(
            expected=HTTPStatus.OK, actual=get_user_me_response.status_code
        )
        get_user_me_response_schema = GetUserMeResponseSchema.model_validate_json(
            get_user_me_response.content
        )
        assert_get_user_me_response(
            register_response=registered_user.response,
            get_user_me_response=get_user_me_response_schema,
        )


@pytest.mark.users
@pytest.mark.negative
class TestUsersNegative:
    @pytest.mark.regression
    def test_get_current_user_without_authorization_returns_401(
        self, auth_client: AuthAPIClient
    ) -> None:
        # Arrange

        # Act
        get_user_me_response = auth_client.get(url=f"{Route.USERS}/me")

        # Assert
        assert_status_code(
            expected=HTTPStatus.UNAUTHORIZED, actual=get_user_me_response.status_code
        )

    @pytest.mark.regression
    def test_get_current_user_with_invalid_token_returns_401(
        self, auth_client: AuthAPIClient
    ) -> None:
        # Arrange
        invalid_headers = {"Authorization": "Bearer invalid-token"}

        # Act
        get_user_me_response = auth_client.get(
            url=f"{Route.USERS}/me",
            headers=invalid_headers,
        )

        # Assert
        assert_status_code(
            expected=HTTPStatus.UNAUTHORIZED, actual=get_user_me_response.status_code
        )

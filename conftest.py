import pytest
from api.auth_api import AuthAPI


@pytest.fixture(scope="session")
def auth_token():
    return AuthAPI().get_auth_token()
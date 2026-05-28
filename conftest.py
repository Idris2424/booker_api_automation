import pytest
from api.auth_api import AuthAPI
from steps.auth_steps import AuthSteps


@pytest.fixture(scope="session")
def auth_token():
    return AuthAPI().get_auth_token()

@pytest.fixture
def auth_steps():
    steps = AuthSteps()
    steps.get_token_with_valid_credentials()
    return steps

@pytest.fixture
def booking_for_auth_test(auth_steps):
    auth_steps.create_booking()
    yield
    auth_steps.delete_booking()
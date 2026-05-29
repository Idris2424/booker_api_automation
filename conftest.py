import pytest
from api.auth_api import AuthAPI
from steps.auth_steps import AuthSteps
from steps.get_booking_steps import GetBookingSteps


@pytest.fixture(scope="session")
def auth_token():
    return AuthAPI().get_auth_token()

@pytest.fixture
def auth_steps():
    steps = AuthSteps()
    steps.get_token_with_valid_credentials()
    return steps

@pytest.fixture
def get_steps(auth_token):
    steps = GetBookingSteps()
    steps.create_booking(auth_token)
    yield steps
    steps.delete_booking(auth_token)
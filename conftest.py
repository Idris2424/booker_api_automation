import pytest
from api.auth_api import AuthAPI
from api.booking_api import BookingAPI


@pytest.fixture(scope="session")
def auth_token():
    return AuthAPI().get_auth_token()

@pytest.fixture
def booking_api(auth_token):
    return BookingAPI(auth_token)

@pytest.fixture
def booking_id(booking_api):
    response = booking_api.create_booking()
    assert "bookingid" in response.json(), "bookingid отсутствует в ответе"
    return response.json()["bookingid"]
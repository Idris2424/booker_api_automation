import pytest
from api.auth_api import AuthAPI
from api.booking_api import BookingAPI


@pytest.fixture(scope="session")
def auth_token():
    auth_api = AuthAPI()
    response = auth_api.get_token()
    assert response.status_code == 200
    token = response.json().get("token")
    assert token is not None
    return token

@pytest.fixture
def booking_api(auth_token):
    return BookingAPI()

@pytest.fixture
def created_booking(booking_api):
    response = booking_api.create_booking()
    assert response.status_code == 200
    assert "bookingid" in response.json()
    booking_id = response.json()["bookingid"]
    return booking_id, response

@pytest.fixture
def booking_id(created_booking):
    booking_id, _ = created_booking
    return booking_id

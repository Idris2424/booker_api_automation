import requests
from data.booker_url import BASE_URL, BOOKING
import jsonschema

from data.booking_data import BOOKING_DATA
from data.bookink_schema import BOOKING_SCHEMA
from data.updated_data import UPDATED_DATA


class BookingAPI:
    def __init__(self):
        self.base_url = BASE_URL

    def create_booking(self):
        url = f"{self.base_url}{BOOKING}"
        response = requests.post(url, json=BOOKING_DATA)
        return response

    def get_booking(self, booking_id):
        url = f"{self.base_url}{BOOKING}/{booking_id}"
        response = requests.get(url)
        return response

    def update_booking(self, booking_id, auth_token):
        url = f"{self.base_url}{BOOKING}/{booking_id}"
        cookies = {"token": auth_token}
        response = requests.put(url, json=UPDATED_DATA, cookies=cookies)
        return response

    def partial_update_booking(self, booking_id, auth_token):
        url = f"{self.base_url}{BOOKING}/{booking_id}"
        cookies = {"token": auth_token}
        response = requests.patch(url, json=UPDATED_DATA, cookies=cookies)
        return response

    def delete_booking(self, booking_id, auth_token):
        url = f"{self.base_url}{BOOKING}/{booking_id}"
        cookies = {"token": auth_token}
        response = requests.delete(url, cookies=cookies)
        return response

    @staticmethod
    def validate_schema():
        jsonschema.validate(instance=BOOKING_DATA, schema=BOOKING_SCHEMA)

    @staticmethod
    def expected_firstname():
        return BOOKING_DATA["firstname"]

    @staticmethod
    def expected_lastname():
        return UPDATED_DATA["lastname"]

    @staticmethod
    def expected_totalprice():
        return UPDATED_DATA["totalprice"]
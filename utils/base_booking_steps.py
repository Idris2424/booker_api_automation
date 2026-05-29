import allure
from api.base_api import BaseAPI
from data.booker_url import BOOKING
from data.booking_data import BOOKING_DATA


class BaseBookingSteps(BaseAPI):

    def __init__(self):
        super().__init__()
        self.booking_id = None

    @allure.step("Создать бронь для теста")
    def create_booking(self, token):
        url = f"{self.base_url}{BOOKING}"
        response = self.post(url, json=BOOKING_DATA)
        self.booking_id = response.json()["bookingid"]
        assert self.booking_id is not None, "booking_id не получен"

    @allure.step("Удалить бронь")
    def delete_booking(self, token):
        url = f"{self.base_url}{BOOKING}/{self.booking_id}"
        self.delete(url, cookies={"token": token})

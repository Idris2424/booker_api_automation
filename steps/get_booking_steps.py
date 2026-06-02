import allure
import jsonschema
from data.booker_url import BOOKING
from data.booking_data import BOOKING_DATA
from data.bookink_schema import BOOKING_SCHEMA
from data.bookings_list_schema import BOOKINGS_LIST_SCHEMA
from utils.base_booking_steps import BaseBookingSteps


class GetBookingSteps(BaseBookingSteps):

    def __init__(self):
        super().__init__()
        self.response = None


    @allure.step("Получить все брони и проверить что список не пустой")
    def get_all_bookings(self):
        url = f"{self.base_url}{BOOKING}"
        self.response = self.get(url)
        self._assert_list_response(self.response.json())

    @allure.step("Получить брони с фильтром firstname={firstname}")
    def get_bookings_by_firstname(self, firstname):
        url = f"{self.base_url}{BOOKING}"
        self.response = self.get(url, params={"firstname": firstname})
        self._assert_list_response(self.response.json())

    @allure.step("Получить брони с фильтром lastname={lastname}")
    def get_bookings_by_lastname(self, lastname):
        url = f"{self.base_url}{BOOKING}"
        self.response = self.get(url, params={"lastname": lastname})
        self._assert_list_response(self.response.json())

    @allure.step("Получить брони с фильтром по датам checkin={checkin} checkout={checkout}")
    def get_bookings_by_dates(self, checkin, checkout):
        url = f"{self.base_url}{BOOKING}"
        self.response = self.get(url, params={"checkin": checkin, "checkout": checkout})
        self._assert_list_response(self.response.json())

    @allure.step("Получить бронь по ID")
    def get_booking_by_id(self, expected_status=200):
        url = f"{self.base_url}{BOOKING}/{self.booking_id}"
        self.response = self.get(url, expected_status=expected_status)

    @allure.step("Проверить данные брони")
    def verify_booking_data(self, data=BOOKING_DATA):
        response_data = self.response.json()
        assert response_data["firstname"] == data["firstname"], \
            f"Ожидался firstname={data['firstname']}, получен {response_data['firstname']}"
        assert response_data["lastname"] == data["lastname"], \
            f"Ожидался lastname={data['lastname']}, получен {response_data['lastname']}"

    @allure.step("Получить несуществующую бронь — ожидаем 404")
    def get_nonexistent_booking(self):
        self.booking_id = 999999
        self.get_booking_by_id(expected_status=404)

    @allure.step("Валидировать схему списка броней")
    def validate_bookings_list_schema(self):
        jsonschema.validate(instance=self.response.json(), schema=BOOKINGS_LIST_SCHEMA)

    @allure.step("Валидировать схему одной брони")
    def validate_booking_schema(self):
        jsonschema.validate(instance=self.response.json(), schema=BOOKING_SCHEMA)

    @allure.step("Проверить заголовки ответа")
    def verify_response_headers(self):
        content_type = self.response.headers.get("Content-Type", "")
        assert "application/json" in content_type, \
            f"Ожидался Content-Type 'application/json', получен '{content_type}'"

    @allure.step("Проверить время ответа < 2 сек")
    def verify_response_time(self):
        elps = self.response.elapsed.total_seconds()
        assert elps < 2.0, f"Время ответа превысило 2 сек: {elps:.2f} сек"

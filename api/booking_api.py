from api.base_api import BaseAPI
from data.booker_url import BASE_URL, BOOKING
import jsonschema
import allure
from data.booking_data import BOOKING_DATA
from data.bookink_schema import BOOKING_SCHEMA
from data.updated_data import UPDATED_DATA


class BookingAPI(BaseAPI):
    def __init__(self, auth_token):
        self.base_url = BASE_URL
        super().__init__()
        self.auth_token = auth_token

    @allure.step("Создать новую бронь")
    def create_booking(self):
        url = f"{self.base_url}{BOOKING}"
        return self.post(url, json=BOOKING_DATA)

    @allure.step("Получить бронь по ID: {booking_id}")
    def get_booking(self, booking_id):
        url = f"{self.base_url}{BOOKING}/{booking_id}"
        return self.get(url)

    @allure.step("Полностью обновить бронь: {booking_id}")
    def update_booking(self, booking_id):
        url = f"{self.base_url}{BOOKING}/{booking_id}"
        return self.put(url, json=UPDATED_DATA, cookies={"token": self.auth_token})

    @allure.step("Частично обновить бронь: {booking_id}")
    def partial_update_booking(self, booking_id):
        url = f"{self.base_url}{BOOKING}/{booking_id}"
        return self.patch(url, json=UPDATED_DATA, cookies={"token": self.auth_token})

    @allure.step("Удалить бронь: {booking_id}")
    def delete_booking(self, booking_id):
        url = f"{self.base_url}{BOOKING}/{booking_id}"
        return self.delete(url, cookies={"token": self.auth_token})

    @staticmethod
    @allure.step("Валидировать схему ответа")
    def validate_schema():
        jsonschema.validate(instance=BOOKING_DATA, schema=BOOKING_SCHEMA)

    @allure.step("Проверяет значение поля response_json[key]")
    def assert_field(self, response_json, key, reference):
        assert response_json[key] == reference[key], \
            f"Поле '{key}': ожидалось '{reference[key]}', получено '{response_json[key]}'"
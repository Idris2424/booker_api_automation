import allure
import jsonschema
from data.booker_url import BOOKING
from data.booking_data import BOOKING_DATA
from data.bookink_schema import BOOKING_SCHEMA
from utils.base_booking_steps import BaseBookingSteps


class PostBookingSteps(BaseBookingSteps):

    def __init__(self):
        super().__init__()
        self.response = None
        self.second_booking_id = None

    @allure.step("Отправить POST /booking")
    def post_booking(self, data=BOOKING_DATA):
        url = f"{self.base_url}{BOOKING}"
        self.response = self.post(url, json=data)
        return self.response

    @allure.step("Проверить что в ответе есть bookingid")
    def verify_booking_created(self):
        data = self.response.json()
        assert "bookingid" in data, "bookingid отсутствует в ответе"
        self.booking_id = data["bookingid"]
        assert self.booking_id is not None, "bookingid не должен быть None"

    @allure.step("Проверить поле {field} равно {value}")
    def verify_field(self, field, value):
        data = self.response.json().get("booking", self.response.json())
        assert data[field] == value, \
            f"Ожидалось {field}={value}, получено {data[field]}"

    @allure.step("Валидировать схему созданной брони")
    def validate_booking_schema(self):
        booking = self.response.json().get("booking", self.response.json())
        jsonschema.validate(instance=booking, schema=BOOKING_SCHEMA)

    @allure.step("Создать вторую бронь и проверить уникальность ID")
    def verify_unique_booking_ids(self, token):
        url = f"{self.base_url}{BOOKING}"
        response2 = self.post(url, json=BOOKING_DATA)
        self.second_booking_id = response2.json()["bookingid"]
        assert self.booking_id != self.second_booking_id, \
            "bookingid двух броней не должны совпадать"
        self.delete(
            f"{self.base_url}{BOOKING}/{self.second_booking_id}",
            cookies={"token": token}
        )

    @allure.step("Получить созданную бронь по ID и проверить данные")
    def verify_booking_accessible_by_get(self, data=BOOKING_DATA):
        url = f"{self.base_url}{BOOKING}/{self.booking_id}"
        response = self.get(url)
        response_data = response.json()
        assert response_data["firstname"] == data["firstname"], \
            f"Ожидался firstname={data['firstname']}, получен {response_data['firstname']}"

import allure
import jsonschema
from data.booker_url import BOOKING
from data.bookink_schema import BOOKING_SCHEMA
from data.updated_data import UPDATED_DATA
from utils.base_booking_steps import BaseBookingSteps


class PutBookingSteps(BaseBookingSteps):

    def __init__(self):
        super().__init__()
        self.response = None
        self.token = None

    @allure.step("Обновить бронь")
    def update_booking(self, data=UPDATED_DATA, expected_status=200, method="put"):
        url = f"{self.base_url}{BOOKING}/{self.booking_id}"
        http_method = self.put if method == "put" else self.patch
        self.response = http_method(
            url,
            expected_status=expected_status,
            json=data,
            cookies={"token": self.token} if self.token else {}
        )
        return self.response

    @allure.step("Проверить поле {field} равно {value}")
    def verify_field(self, field, value):
        data = self.response.json()
        assert data[field] == value, \
            f"Ожидалось {field}={value}, получено {data[field]}"

    @allure.step("Проверить что все поля обновились")
    def verify_all_fields_updated(self, data=UPDATED_DATA):
        response_data = self.response.json()
        for field in ["firstname", "lastname", "totalprice", "depositpaid"]:
            assert response_data[field] == data[field], \
                f"Ожидалось {field}={data[field]}, получено {response_data[field]}"

    @allure.step("Валидировать схему ответа после обновления")
    def validate_booking_schema(self):
        jsonschema.validate(instance=self.response.json(), schema=BOOKING_SCHEMA)

    @allure.step("Обновить несуществующую бронь — ожидаем 404")
    def put_nonexistent_booking(self):
        url = f"{self.base_url}{BOOKING}/999999"
        self.response = self.put(
            url,
            expected_status=405,
            json=UPDATED_DATA,
            cookies={"token": self.token}
        )

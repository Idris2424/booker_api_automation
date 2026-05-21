import allure

from api.booking_api import BookingAPI
from data.booking_data import BOOKING_DATA
from data.updated_data import UPDATED_DATA


class BookingSteps(BookingAPI):

    def __init__(self, auth_token):
        super().__init__(auth_token)
        self.booking_id = None

    @allure.step("Получить токен авторизации")
    def get_token(self, auth_token):
        assert auth_token is not None, "Токен не получен"

    @allure.step("Создать новую бронь и сохранить bookingid")
    def create_booking(self):
        response = super().create_booking()
        assert "bookingid" in response.json(), "bookingid отсутствует в ответе"
        self.booking_id = response.json()["bookingid"]
        assert self.booking_id is not None, "booking_id не получен"

    @allure.step("Получить созданную бронь по ID")
    def get_booking(self, expected_status=200):
        response = super().get_booking(self.booking_id)
        self.assert_field(response.json(), "firstname", BOOKING_DATA)

    @allure.step("Валидировать схему ответа")
    def validate_schema(self):
        super().validate_schema()

    @allure.step("Обновить бронь (полное обновление)")
    def full_update(self):
        response = super().update_booking(self.booking_id)
        self.assert_field(response.json(), "firstname", UPDATED_DATA)

    @allure.step("Проверить обновление")
    def verify_update(self):
        response = super().get_booking(self.booking_id)
        self.assert_field(response.json(), "lastname", UPDATED_DATA)

    @allure.step("Частично обновить бронь (PATCH)")
    def partial_update(self):
        response = super().partial_update_booking(self.booking_id)
        self.assert_field(response.json(), "totalprice", UPDATED_DATA)
        self.assert_field(response.json(), "lastname", UPDATED_DATA)

    @allure.step("Проверить время ответа")
    def verify_response_time(self):
        response = super().get_booking(self.booking_id)
        elapsed = response.elapsed.total_seconds()
        assert elapsed < 2.0, f"Время ответа превысило 2 сек: {elapsed:.2f} сек"

    @allure.step("Проверить заголовок ответа")
    def verify_response_header(self):
        response = super().get_booking(self.booking_id)
        content_type = response.headers["Content-Type"]
        assert "application/json" in content_type, \
            f"Ожидался Content-Type 'application/json', получен '{content_type}'"

    @allure.step("Удалить бронь")
    def delete_booking(self):
        super().delete_booking(self.booking_id)

    @allure.step("Проверить удаление")
    def verify_deletion(self):
        super().get_booking(self.booking_id, expected_status=404)

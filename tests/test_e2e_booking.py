import allure

from data.booking_data import BOOKING_DATA
from data.updated_data import UPDATED_DATA


class TestBookingE2E:

    @allure.title("1. Получить токен авторизации")
    def test_verify_token(self, auth_token):
        assert auth_token is not None

    @allure.title("2-3. Создать новую бронь и сохранить bookingid")
    def test_create_booking(self, created_booking):
        assert created_booking is not None, "booking_id не получен"

    @allure.title("4. Получить созданную бронь по ID")
    def test_get_booking(self, booking_api, booking_id):
        response = booking_api.get_booking(booking_id)
        booking_api.assert_field(response.json(), "firstname", BOOKING_DATA)

    @allure.title("5. Валидировать схему ответа")
    def test_validate_schema(self, booking_api):
        booking_api.validate_schema()

    @allure.title("6. Обновить бронь (полное обновление)")
    def test_full_update(self, booking_api, booking_id):
        response = booking_api.update_booking(booking_id)
        booking_api.assert_field(response.json(), "firstname", UPDATED_DATA)

    @allure.title("7. Проверить обновление")
    def test_verify_update(self, booking_api, booking_id):
        response = booking_api.update_booking(booking_id)
        booking_api.assert_field(response.json(), "lastname", UPDATED_DATA)

    @allure.title("8. Частично обновить бронь (PATCH)")
    def test_partial_update(self, booking_api, booking_id):
        response = booking_api.partial_update_booking(booking_id)
        booking_api.assert_field(response.json(), "totalprice", UPDATED_DATA)
        booking_api.assert_field(response.json(), "lastname", UPDATED_DATA)

    @allure.title("9. Удалить бронь")
    def test_delete_booking(self, booking_api, booking_id):
        booking_api.delete_booking(booking_id)

    @allure.title("10. Проверить удаление")
    def test_verify_deletion(self, booking_api, booking_id):
        booking_api.get_booking(booking_id, expected_status=404)

    @allure.title("11. Проверить время ответа")
    def test_response_time(self, booking_api, booking_id):
        response = booking_api.get_booking(booking_id)
        elapsed = response.elapsed.total_seconds()
        assert elapsed < 2.0, f"Время ответа превысило 2 сек: {elapsed:.2f} сек"

    @allure.title("12. Проверить заголовок ответа")
    def test_response_content_type(self, booking_api, booking_id):
        response = booking_api.get_booking(booking_id)
        content_type = response.headers["Content-Type"]
        assert "application/json" in content_type, \
            f"Ожидался Content-Type 'application/json', получен '{content_type}'"

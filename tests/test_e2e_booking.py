import allure
import pytest
from data.booking_data import BOOKING_DATA
from data.updated_data import UPDATED_DATA


class TestBookingE2E:

    @allure.title("E2E: полный цикл бронирования")
    def test_booking_e2e(self, booking_api, auth_token, booking_id):

        with allure.step("1. Получить токен авторизации"):
            assert auth_token is not None

        with allure.step("2-3. Создать новую бронь и сохранить bookingid"):
            response = booking_api.create_booking()
            assert "bookingid" in response.json(), "bookingid отсутствует в ответе"
            booking_id = response.json()["bookingid"]
            assert booking_id is not None, "booking_id не получен"

        with allure.step("4. Получить созданную бронь по ID"):
            response = booking_api.get_booking(booking_id)
            booking_api.assert_field(response.json(), "firstname", BOOKING_DATA)

        with allure.step("5. Валидировать схему ответа"):
            booking_api.validate_schema()

        with allure.step("6. Обновить бронь (полное обновление)"):
            response = booking_api.update_booking(booking_id)
            booking_api.assert_field(response.json(), "firstname", UPDATED_DATA)

        with allure.step("7. Проверить обновление"):
            response = booking_api.get_booking(booking_id)
            booking_api.assert_field(response.json(), "lastname", UPDATED_DATA)

        with allure.step("8. Частично обновить бронь (PATCH)"):
            response = booking_api.partial_update_booking(booking_id)
            booking_api.assert_field(response.json(), "totalprice", UPDATED_DATA)
            booking_api.assert_field(response.json(), "lastname", UPDATED_DATA)

        with allure.step("11. Проверить время ответа"):
            response = booking_api.get_booking(booking_id)
            elapsed = response.elapsed.total_seconds()
            assert elapsed < 2.0, f"Время ответа превысило 2 сек: {elapsed:.2f} сек"

        with allure.step("12. Проверить заголовок ответа"):
            response = booking_api.get_booking(booking_id)
            content_type = response.headers["Content-Type"]
            assert "application/json" in content_type, \
                f"Ожидался Content-Type 'application/json', получен '{content_type}'"

        with allure.step("9. Удалить бронь"):
            booking_api.delete_booking(booking_id)

        with allure.step("10. Проверить удаление"):
            booking_api.get_booking(booking_id, expected_status=404)

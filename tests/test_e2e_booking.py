import allure
from data.updated_data import UPDATED_DATA


@allure.epic("E2E Booking")
@allure.feature("Full booking cycle")
class TestsBooker:

    @allure.step("1. Получить токен авторизации")
    def test_verify_token(self, auth_token):
        assert auth_token is not None

    @allure.step("2-3. Создать новую бронь и Сохранить bookingid")
    def test_create_booking(self, created_booking):
        assert created_booking is not None

    @allure.step("4. Получить созданную бронь по ID")
    def test_get_booking(self,booking_api, booking_id):
        response = booking_api.get_booking(booking_id)
        assert response.status_code == 200
        assert response.json()["firstname"] == booking_api.expected_firstname()

    @allure.step("5. Валидировать схему ответа")
    def test_validate_schema(self, booking_api):
        booking_api.validate_schema()

    @allure.step("6. Обновить бронь (полное обновление)")
    def test_full_update(self, booking_api, booking_id, auth_token):
        response = booking_api.update_booking(booking_id, auth_token)
        assert response.status_code == 200
        assert response.json()["firstname"] == UPDATED_DATA["firstname"]

    @allure.step("7. Проверить обновление")
    def test_verify_update(self, booking_api, booking_id, auth_token):
        response = booking_api.update_booking(booking_id, auth_token)
        assert response.status_code == 200
        assert response.json()["lastname"] == booking_api.expected_lastname()

    @allure.step("8. Частично обновить бронь (PATCH)")
    def test_partial_update(self, booking_api, booking_id, auth_token):
        response = booking_api.partial_update_booking(booking_id, auth_token)
        assert response.status_code == 200
        assert response.json()["totalprice"] == booking_api.expected_totalprice()
        assert response.json()["lastname"] == booking_api.expected_lastname()

    @allure.step("9. Удалить бронь")
    def test_delete_booking(self, booking_api, booking_id, auth_token):
        response = booking_api.delete_booking(booking_id, auth_token)
        assert response.status_code == 201

    @allure.step("10. Проверить удаление")
    def test_verify_deletion(self, booking_api, booking_id):
        response = booking_api.get_booking(booking_id)
        assert response.status_code == 404

    @allure.step("11. Проверить время ответа")
    def test_response_time(self, booking_api, booking_id):
        response = booking_api.get_booking(booking_id)
        assert response.elapsed.total_seconds() < 2.0

    @allure.step("12. Проверить заголовок ответа")
    def test_response_content_type(self, booking_api, booking_id):
        response = booking_api.get_booking(booking_id)
        assert "application/json" in response.headers["Content-Type"]

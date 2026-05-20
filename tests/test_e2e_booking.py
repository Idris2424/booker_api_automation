import allure

from api.booking_api import BookingAPI
from steps.booking_steps import BookingSteps


class TestBookingE2E:

    @allure.title("E2E: полный цикл бронирования")
    def test_booking_e2e(self, auth_token):
        steps = BookingSteps(auth_token)

        # 1. Получить токен авторизации
        steps.verify_token(auth_token)

        # 2-3. Создать новую бронь и сохранить bookingid
        booking_id = steps.create_booking()

        # 4. Получить созданную бронь по ID
        steps.get_booking(booking_id)

        # 5. Валидировать схему ответа
        steps.validate_schema()

        # 6. Обновить бронь (полное обновление)
        steps.full_update(booking_id)

        # 7. Проверить обновление
        steps.verify_update(booking_id)

        # 8. Частично обновить бронь (PATCH)
        steps.partial_update(booking_id)

        # 9. Проверить время ответа
        steps.verify_response_time(booking_id)

        # 10. Проверить заголовок ответа
        steps.verify_content_type(booking_id)

        # 11. Удалить бронь
        steps.delete_booking(booking_id)

        # 12. Проверить удаление
        steps.verify_deletion(booking_id)

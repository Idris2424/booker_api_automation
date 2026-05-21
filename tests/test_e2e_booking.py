import allure
from steps.booking_steps import BookingSteps


class TestBookingE2E:

    @allure.title("E2E: полный цикл бронирования")
    def test_booking_e2e(self, auth_token):
        steps = BookingSteps(auth_token)

        # 1. Получить токен авторизации
        steps.get_token(auth_token)

        # 2-3. Создать новую бронь и сохранить bookingid
        steps.create_booking()

        # 4. Получить созданную бронь по ID
        steps.get_booking()

        # 5. Валидировать схему ответа
        steps.validate_schema()

        # 6. Обновить бронь (полное обновление)
        steps.full_update()

        # 7. Проверить обновление
        steps.verify_update()

        # 8. Частично обновить бронь (PATCH)
        steps.partial_update()

        # 9. Проверить время ответа
        steps.verify_response_time()

        # 10. Проверить заголовок ответа
        steps.verify_response_header()

        # 11. Удалить бронь
        steps.delete_booking()

        # 12. Проверить удаление
        steps.verify_deletion()

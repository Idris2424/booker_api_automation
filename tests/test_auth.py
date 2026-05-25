import allure
from steps.auth_steps import AuthSteps


class TestAuth:

    @allure.title("TC_AUTH_001: Получение токена с валидными данными")
    def test_get_token_valid_credentials(self):
        steps = AuthSteps()
        steps.get_token_with_valid_credentials()

    @allure.title("TC_AUTH_002: Токен с неверным паролем не работает для защищённых запросов")
    def test_invalid_password_token(self, auth_token):
        steps = AuthSteps()

        steps.create_booking_for_test(auth_token)
        steps.get_token_with_wrong_password()
        steps.verify_invalid_token()
        steps.delete_booking_after_test(auth_token)

    @allure.title("TC_AUTH_003: Токен с несуществующим пользователем невалиден")
    def test_fake_user_token(self, auth_token):
        steps = AuthSteps()

        steps.create_booking_for_test(auth_token)
        steps.get_token_with_fake_user()
        steps.verify_invalid_token()
        steps.delete_booking_after_test(auth_token)

    @allure.title("TC_AUTH_004: Использование валидного токена для PUT /booking/{id}")
    def test_valid_token_allows_protected_request(self, auth_token):
        steps = AuthSteps()

        steps.create_booking_for_test(auth_token)
        steps.token = auth_token
        steps.use_valid_token_for_protected_request()
        steps.delete_booking_after_test(auth_token)

    @allure.title("TC_AUTH_005: Использование неверного токена возвращает 403")
    def test_invalid_token_returns_403(self, auth_token):
        steps = AuthSteps()

        steps.create_booking_for_test(auth_token)
        steps.use_invalid_token_for_protected_request()
        steps.delete_booking_after_test(auth_token)

    @allure.title("TC_AUTH_006: Запрос без токена к защищённому эндпоинту возвращает 403")
    def test_no_token_returns_403(self, auth_token):
        steps = AuthSteps()

        steps.create_booking_for_test(auth_token)
        steps.request_without_token()
        steps.delete_booking_after_test(auth_token)

    @allure.title("TC_AUTH_007: Валидация формата токена — строка, не пустая")
    def test_token_format_is_valid(self):
        steps = AuthSteps()

        steps.get_token_with_valid_credentials()
        steps.validate_token_format()

    @allure.title("TC_AUTH_008: Повторное получение токена — оба валидны (идемпотентность)")
    def test_token_idempotency(self):
        steps = AuthSteps()

        steps.get_token_twice_and_verify_both()
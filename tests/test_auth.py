import allure
from data.auth_data import AUTH_DATA_WRONG_PASS, AUTH_DATA_WRONG_USERNAME


class TestAuth:

    @allure.title("TC_AUTH_001: Получение токена с валидными данными")
    def test_get_token_valid_credentials(self, auth_steps):
        auth_steps.get_token_with_valid_credentials()

    @allure.title("TC_AUTH_002: Токен с неверным паролем не работает для защищённых запросов")
    def test_invalid_password_token(self, auth_steps):
        invalid_token = auth_steps.get_token(AUTH_DATA_WRONG_PASS)
        auth_steps.verify_invalid_token(invalid_token)

    @allure.title("TC_AUTH_003: Токен с несуществующим пользователем невалиден")
    def test_fake_user_token(self, auth_steps):
        invalid_token = auth_steps.get_token_with_invalid_credentials(AUTH_DATA_WRONG_USERNAME)
        auth_steps.verify_invalid_token(invalid_token)

    @allure.title("TC_AUTH_004: Использование валидного токена для PUT /booking/{id}")
    def test_valid_token_allows_protected_request(self, auth_steps):
        auth_steps.put_booking_with_valid_token()

    @allure.title("TC_AUTH_005: Использование неверного токена возвращает 403")
    def test_invalid_token_returns_403(self, auth_steps):
        auth_steps.put_booking_with_token(token="invalid", expected_status=403)

    @allure.title("TC_AUTH_006: Запрос без токена к защищённому эндпоинту возвращает 403")
    def test_no_token_returns_403(self, auth_steps):
        auth_steps.put_booking_with_token(token=None, expected_status=403)

    @allure.title("TC_AUTH_007: Валидация формата токена — строка, не пустая")
    def test_token_format_is_valid(self, auth_steps):
        auth_steps.validate_token_format()

    @allure.title("TC_AUTH_008: Повторное получение токена — оба валидны (идемпотентность)")
    def test_token_idempotency(self, auth_steps):
        auth_steps.get_token_twice_and_verify_both()

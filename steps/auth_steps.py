import allure
from data.auth_data import AUTH_DATA
from data.booker_url import BOOKING
from data.updated_data import UPDATED_DATA
from utils.base_booking_steps import BaseBookingSteps


class AuthSteps(BaseBookingSteps):

    def __init__(self):
        super().__init__()
        self.token = None


    @allure.step("Получить токен")
    def get_token(self, credentials=AUTH_DATA):
        url = f"{self.base_url}/auth"
        response = self.post(url, expected_status=200, json=credentials)
        token = response.json().get("token")
        return token

    @allure.step("Получить токен с валидными данными и проверить статус 200")
    def get_token_with_valid_credentials(self):
        token = self.get_token()
        assert token is not None, "Токен отсутствует в ответе"
        self.token = token
        return self.token

    @allure.step("Отправить PUT запрос с токеном")
    def put_booking_with_token(self, token, expected_status=200, data=UPDATED_DATA):
        url = f"{self.base_url}{BOOKING}/{self.booking_id}"
        response = self.put(
            url,
            expected_status=expected_status,
            json=data,
            cookies={"token": token} if token else {}
        )
        if 200 <= expected_status < 300:
            assert response.json()["firstname"] == data["firstname"], \
                "Данные брони не обновились после PUT с валидным токеном"
        return response

    @allure.step("Использовать валидный токен для PUT /booking")
    def put_booking_with_valid_token(self):
        self.put_booking_with_token(token=self.token, expected_status=200)

    @allure.step("Проверить формат токена: строка, не пустая")
    def validate_token_format(self):
        assert isinstance(self.token, str), \
            f"Токен должен быть строкой, получен {type(self.token)}"
        assert len(self.token) > 0, "Токен не должен быть пустым"

    @allure.step("Получить токен повторно и убедиться, что оба валидны")
    def get_token_twice_and_verify_both(self):
        first_token = self.get_token()
        second_token = self.get_token()
        assert first_token is not None, "Первый токен не получен"
        assert second_token is not None, "Второй токен не получен"
        assert isinstance(first_token, str) and len(first_token) > 0, \
            "Первый токен невалидного формата"
        assert isinstance(second_token, str) and len(second_token) > 0, \
            "Второй токен невалидного формата"
        return first_token, second_token

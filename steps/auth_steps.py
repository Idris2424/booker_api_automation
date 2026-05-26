import allure
from api.auth_api import AuthAPI
from data.booker_url import BOOKING
from data.booking_data import BOOKING_DATA
from data.updated_data import UPDATED_DATA


class AuthSteps(AuthAPI):

    def __init__(self):
        super().__init__()
        self.token = None
        self.booking_id = None
        self.valid_token = None


    @allure.step("Создать бронь для auth-тестов")
    def create_booking_for_test(self):
        url = f"{self.base_url}{BOOKING}"
        response = self.post(url, json=BOOKING_DATA)
        self.booking_id = response.json()["bookingid"]
        assert self.booking_id is not None, "booking_id не получен"

    @allure.step("Удалить бронь после теста")
    def delete_booking_after_test(self):
        url = f"{self.base_url}{BOOKING}/{self.booking_id}"
        self.delete(url, cookies={"token": self.valid_token})

    @allure.step("Получить токен с валидными данными и проверить статус 200")
    def get_token_with_valid_credentials(self):
        self.token = self.get_auth_token()
        self.valid_token = self.token
        assert self.token is not None, "Токен отсутствует в ответе"
        return self.token

    @allure.step("Получить токен с невалидными данными")
    def get_token_with_invalid_credentials(self, credentials):
        url = f"{self.base_url}/auth"
        response = self.post(url, expected_status=200, json=credentials)
        invalid_token = response.json().get("token")
        return invalid_token

    @allure.step("Убедиться, что токен от неверного пароля не работает для защищённых запросов")
    def verify_invalid_token(self, invalid_token):
        url = f"{self.base_url}{BOOKING}/{self.booking_id}"
        self.put(
            url,
            expected_status=403,
            json=UPDATED_DATA,
            cookies={"token": invalid_token}
        )

    @allure.step("Отправить PUT запрос с токеном")
    def put_booking_with_token(self, token, expected_status=200):
        url = f"{self.base_url}{BOOKING}/{self.booking_id}"
        response = self.put(
            url,
            expected_status=expected_status,
            json=UPDATED_DATA,
            cookies={"token": token} if token else {}
        )
        if expected_status == 200:
            assert response.json()["firstname"] == UPDATED_DATA["firstname"], \
                "Данные брони не обновились после PUT с валидным токеном"
        return response


    @allure.step("Использовать валидный токен для PUT /booking")
    def put_booking_with_valid_token(self):
        self.put_booking_with_token(token=self.token, expected_status=200)


    @allure.step("Отправить PUT без токена — ожидаем 403")
    def request_without_token(self):
        url = f"{self.base_url}{BOOKING}/{self.booking_id}"
        response = self.put(
            url,
            expected_status=403,
            json=UPDATED_DATA
        )
        return response


    @allure.step("Проверить формат токена: строка, не пустая")
    def validate_token_format(self):
        assert isinstance(self.token, str), \
            f"Токен должен быть строкой, получен {type(self.token)}"
        assert len(self.token) > 0, "Токен не должен быть пустой"


    @allure.step("Получить токен повторно и убедиться, что оба валидны")
    def get_token_twice_and_verify_both(self):
        first_token = self.get_auth_token()
        second_token = self.get_auth_token()
        assert first_token is not None, "Первый токен не получен"
        assert second_token is not None, "Второй токен не получен"
        assert isinstance(first_token, str) and len(first_token) > 0, \
            "Первый токен невалидного формата"
        assert isinstance(second_token, str) and len(second_token) > 0, \
            "Второй токен невалидного формата"
        return first_token, second_token

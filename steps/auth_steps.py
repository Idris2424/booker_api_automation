import allure
from api.auth_api import AuthAPI
from api.booking_api import BookingAPI
from data.auth_data import AUTH_DATA_WRONG_PASS, AUTH_DATA_WRONG_USERNAME
from data.booker_url import BOOKING
from data.updated_data import UPDATED_DATA


class AuthSteps(AuthAPI):

    def __init__(self):
        super().__init__()
        self.token = None
        self.booking_id = None


    @allure.step("Создать бронь для auth-тестов")
    def create_booking_for_test(self, auth_token):
        booking_api = BookingAPI(auth_token)
        response = booking_api.create_booking()
        self.booking_id = response.json()["bookingid"]
        assert self.booking_id is not None, "booking_id не получен"

    @allure.step("Удалить бронь после теста")
    def delete_booking_after_test(self, auth_token):
        BookingAPI(auth_token).delete_booking(self.booking_id)


    @allure.step("Получить токен с валидными данными и проверить статус 200")
    def get_token_with_valid_credentials(self):
        self.token = self.get_auth_token()
        assert self.token is not None, "Токен отсутствует в ответе"
        return self.token


    @allure.step("Получить токен с неверным паролем")
    def get_token_with_wrong_password(self):
        url = f"{self.base_url}/auth"
        response = self.post(url, expected_status=200, json=AUTH_DATA_WRONG_PASS)
        self.token = response.json().get("token")
        return self.token

    @allure.step("Убедиться, что токен от неверного пароля не работает для защищённых запросов")
    def verify_invalid_token(self):
        url = f"{self.base_url}{BOOKING}/{self.booking_id}"
        response = self.put(
            url,
            expected_status=403,
            json=UPDATED_DATA,
            cookies={"token": self.token}
        )
        return response


    @allure.step("Получить токен с несуществующим пользователем")
    def get_token_with_fake_user(self):
        url = f"{self.base_url}/auth"
        response = self.post(url, expected_status=200, json=AUTH_DATA_WRONG_USERNAME)
        self.token = response.json().get("token")
        return self.token


    @allure.step("Использовать валидный токен для PUT /booking")
    def use_valid_token_for_protected_request(self):
        url = f"{self.base_url}{BOOKING}/{self.booking_id}"
        response = self.put(
            url,
            expected_status=200,
            json=UPDATED_DATA,
            cookies={"token": self.token}
        )
        assert response.json()["firstname"] == UPDATED_DATA["firstname"], \
            "Данные брони не обновились"
        return response


    @allure.step("Использовать неверный токен для PUT — ожидаем 403")
    def use_invalid_token_for_protected_request(self):
        url = f"{self.base_url}{BOOKING}/{self.booking_id}"
        response = self.put(
            url,
            expected_status=403,
            json=UPDATED_DATA,
            cookies={"token": "invalid"}
        )
        return response


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

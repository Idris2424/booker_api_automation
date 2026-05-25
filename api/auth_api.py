from api.base_api import BaseAPI
from data.booker_url import BASE_URL, AUTH
from data.auth_data import AUTH_DATA

class AuthAPI(BaseAPI):
    def get_auth_token(self) :
        url = f"{self.base_url}{AUTH}"
        response = self.post(url, expected_status=200, json=AUTH_DATA)
        token = response.json().get("token")
        assert token is not None, "Токен отсутствует в ответе"
        return token

import requests
from data.booker_url import BASE_URL, AUTH
from data.auth_data import AUTH_DATA

def get_auth_token() -> str:
    url = f"{BASE_URL}{AUTH}"
    response = requests.post(url, json=AUTH_DATA)
    assert response.status_code == 200, \
        f"Не удалось получить токен, статус: {response.status_code}"
    token = response.json().get("token")
    assert token is not None, "Токен отсутствует в ответе"
    return token
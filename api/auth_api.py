import requests
from data.booker_url import BASE_URL, AUTH


class AuthAPI:
    def __init__(self):
        self.base_url = BASE_URL

    def get_token(self):
        url = f"{self.base_url}{AUTH}"
        payload = {
            "username": "admin",
            "password": "password123"
        }
        response = requests.post(url, json=payload)
        return response
import requests
from data.booker_url import BASE_URL

class BaseAPI:
    def __init__(self):
        self.base_url = BASE_URL

    def _check_status(self, response, url, method, expected_status):
        assert response.status_code == expected_status, \
            f"{method} {url} — ожидался статус {expected_status}, получен {response.status_code}"

    def get(self, url, expected_status=200, **kwargs):
        response = requests.get(url, **kwargs)
        self._check_status(response, url, "GET", expected_status)
        return response

    def post(self, url, expected_status=200, **kwargs):
        response = requests.post(url, **kwargs)
        self._check_status(response, url, "POST", expected_status)
        return response

    def put(self, url, expected_status=200, **kwargs):
        response = requests.put(url, **kwargs)
        self._check_status(response, url, "PUT", expected_status)
        return response

    def patch(self, url, expected_status=200, **kwargs):
        response = requests.patch(url, **kwargs)
        self._check_status(response, url, "PATCH", expected_status)
        return response

    def delete(self, url, expected_status=201, **kwargs):
        response = requests.delete(url, **kwargs)
        self._check_status(response, url, "DELETE", expected_status)
        return response
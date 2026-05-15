import requests
from data.booker_url import BASE_URL

class BaseAPI:
    def __init__(self):
        self.base_url = BASE_URL

    def get(self, url, expected_status=200, **kwargs):
        response = requests.get(url, **kwargs)
        assert response.status_code == expected_status, \
            f"GET {url} — ожидался статус {expected_status}, получен {response.status_code}"
        return response

    def post(self, url, expected_status=200, **kwargs):
        response = requests.post(url, **kwargs)
        assert response.status_code == expected_status, \
            f"POST {url} — ожидался статус {expected_status}, получен {response.status_code}"
        return response

    def put(self, url, expected_status=200, **kwargs):
        response = requests.put(url, **kwargs)
        assert response.status_code == expected_status, \
            f"PUT {url} — ожидался статус {expected_status}, получен {response.status_code}"
        return response

    def patch(self, url, expected_status=200, **kwargs):
        response = requests.patch(url, **kwargs)
        assert response.status_code == expected_status, \
            f"PATCH {url} — ожидался статус {expected_status}, получен {response.status_code}"
        return response

    def delete(self, url, expected_status=201, **kwargs):
        response = requests.delete(url, **kwargs)
        assert response.status_code == expected_status, \
            f"DELETE {url} — ожидался статус {expected_status}, получен {response.status_code}"
        return response
import allure
import pytest


class TestGetBooking:

    @allure.title("TC_GET_001: Получение всех броней")
    def test_get_all_bookings(self, get_steps):
        get_steps.get_all_bookings()
        get_steps.verify_response_time()

    @allure.title("TC_GET_002: Фильтрация по firstname")
    def test_filter_by_firstname(self, get_steps):
        get_steps.get_bookings_by_firstname("John")

    @allure.title("TC_GET_003: Фильтрация по lastname")
    def test_filter_by_lastname(self, get_steps):
        get_steps.get_bookings_by_lastname("Doe")

    @allure.title("TC_GET_004: Фильтрация по датам checkin/checkout")
    def test_filter_by_dates(self, get_steps):
        get_steps.get_bookings_by_dates(checkin="2026-05-01", checkout="2026-06-30")

    @allure.title("TC_GET_005: Получение существующей брони по ID")
    def test_get_booking_by_id(self, get_steps):
        get_steps.get_booking_by_id()
        get_steps.validate_booking_schema()

    @allure.title("TC_GET_006: Получение несуществующей брони по ID")
    def test_get_nonexistent_booking(self, get_steps):
        get_steps.get_nonexistent_booking()

    @allure.title("TC_GET_007: Валидация схемы списка броней")
    def test_validate_bookings_list_schema(self, get_steps):
        get_steps.get_all_bookings()
        get_steps.validate_bookings_list_schema()

    @allure.title("TC_GET_008: Валидация схемы одной брони")
    def test_validate_booking_schema(self, get_steps):
        get_steps.get_booking_by_id()
        get_steps.validate_booking_schema()

    @allure.title("TC_GET_009: Проверка заголовков ответа")
    def test_response_headers(self, get_steps):
        get_steps.get_all_bookings()
        get_steps.verify_response_headers()

    @allure.title("TC_GET_010: Проверка времени ответа")
    def test_response_time(self, get_steps):
        get_steps.get_all_bookings()
        get_steps.verify_response_time()

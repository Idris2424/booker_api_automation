import allure
import pytest
from data.booking_data import (
    MINIMAL_BOOKING_DATA,
    INVALID_DATES_DATA,
    EMPTY_FIRSTNAME_DATA,
    LONG_LASTNAME_DATA
)


class TestPostBooking:

    @allure.title("TC_POST_001: Создание валидной брони")
    def test_create_valid_booking(self, post_steps):
        post_steps.post_booking()
        post_steps.verify_booking_created()

    @allure.title("TC_POST_002: Создание брони с минимальными полями")
    def test_create_booking_minimal_fields(self, post_steps):
        post_steps.post_booking(data=MINIMAL_BOOKING_DATA)
        post_steps.verify_booking_created()

    @allure.title("TC_POST_003: Создание брони с depositpaid=false")
    def test_create_booking_deposit_false(self, post_steps):
        post_steps.post_booking(data={**MINIMAL_BOOKING_DATA, "depositpaid": False})
        post_steps.verify_booking_created()
        post_steps.verify_field("depositpaid", False)

    @allure.title("TC_POST_004: Создание брони с additionalneeds")
    def test_create_booking_with_additionalneeds(self, post_steps):
        post_steps.post_booking(data={**MINIMAL_BOOKING_DATA, "additionalneeds": "breakfast"})
        post_steps.verify_booking_created()
        post_steps.verify_field("additionalneeds", "breakfast")

    @allure.title("TC_POST_005: Создание брони с невалидными датами (checkin после checkout)")
    def test_create_booking_invalid_dates(self, post_steps):
        post_steps.post_booking(data=INVALID_DATES_DATA)
        post_steps.verify_booking_created()

    @allure.title("TC_POST_006: Создание брони с пустым firstname")
    def test_create_booking_empty_firstname(self, post_steps):
        post_steps.post_booking(data=EMPTY_FIRSTNAME_DATA)
        post_steps.verify_booking_created()
        post_steps.verify_field("firstname", "")

    @allure.title("TC_POST_007: Создание брони с очень длинным lastname")
    def test_create_booking_long_lastname(self, post_steps):
        post_steps.post_booking(data=LONG_LASTNAME_DATA)
        post_steps.verify_booking_created()

    @allure.title("TC_POST_008: Валидация схемы созданной брони")
    def test_validate_booking_schema(self, post_steps):
        post_steps.post_booking()
        post_steps.verify_booking_created()
        post_steps.validate_booking_schema()

    @allure.title("TC_POST_009: Проверка уникальности bookingid")
    def test_unique_booking_ids(self, post_steps, auth_token):
        post_steps.post_booking()
        post_steps.verify_booking_created()
        post_steps.verify_unique_booking_ids(auth_token)

    @allure.title("TC_POST_010: Проверка что созданная бронь доступна по GET")
    def test_booking_accessible_by_get(self, post_steps):
        post_steps.post_booking()
        post_steps.verify_booking_created()
        post_steps.verify_booking_accessible_by_get()

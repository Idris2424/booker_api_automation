import allure
import pytest
from data.updated_data import UPDATED_DATA, NEW_DATES


class TestPutBooking:

    @allure.title("TC_PUT_001: Полное обновление брони (PUT) с токеном")
    def test_full_update_with_token(self, put_steps):
        put_steps.update_booking()
        put_steps.verify_all_fields_updated()

    @allure.title("TC_PUT_002: Частичное обновление брони (PATCH) с токеном")
    def test_partial_update_with_token(self, put_steps):
        put_steps.update_booking(data={"firstname": "Anvar"}, method="patch")
        put_steps.verify_field("firstname", "Anvar")

    @allure.title("TC_PUT_003: Обновление несуществующей брони — ожидаем 404")
    def test_update_nonexistent_booking(self, put_steps):
        put_steps.put_nonexistent_booking()

    @allure.title("TC_PUT_004: Обновление без токена — ожидаем 403")
    def test_update_without_token(self, put_steps):
        put_steps.token = None
        put_steps.update_booking(expected_status=403)

    @allure.title("TC_PUT_005: Обновление с неверным токеном — ожидаем 403")
    def test_update_with_invalid_token(self, put_steps):
        put_steps.token = "invalid"
        put_steps.update_booking(expected_status=403)

    @allure.title("TC_PUT_006: Обновление с пустым firstname")
    def test_update_empty_firstname(self, put_steps):
        put_steps.update_booking(data={**UPDATED_DATA, "firstname": ""})
        put_steps.verify_field("firstname", "")

    @allure.title("TC_PUT_007: Обновление дат брони")
    def test_update_booking_dates(self, put_steps):
        put_steps.update_booking(data=NEW_DATES)
        put_steps.verify_field("bookingdates", NEW_DATES["bookingdates"])

    @allure.title("TC_PUT_008: Валидация схемы после обновления")
    def test_validate_schema_after_update(self, put_steps):
        put_steps.update_booking()
        put_steps.validate_booking_schema()

    @allure.title("TC_PATCH_001: PATCH — обновление только totalprice")
    def test_patch_totalprice(self, put_steps):
        put_steps.update_booking(data={"totalprice": 500}, method="patch")
        put_steps.verify_field("totalprice", 500)

    @allure.title("TC_PATCH_002: PATCH — обновление только depositpaid")
    def test_patch_depositpaid(self, put_steps):
        put_steps.update_booking(data={"depositpaid": False}, method="patch")
        put_steps.verify_field("depositpaid", False)

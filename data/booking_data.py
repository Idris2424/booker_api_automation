BOOKING_DATA = {
    "firstname": "John",
    "lastname": "Doe",
    "totalprice": 100,
    "depositpaid": True,
    "bookingdates": {
        "checkin": "2026-05-06",
        "checkout": "2026-06-14"
    },
    "additionalneeds": "Breakfast"
}
MINIMAL_BOOKING_DATA = {
    "firstname": "John",
    "lastname": "Doe",
    "totalprice": 100,
    "depositpaid": True,
    "bookingdates": {
        "checkin": "2026-05-06",
        "checkout": "2026-06-14"
    }
}

INVALID_DATES_DATA = {
    **BOOKING_DATA,
    "bookingdates": {
        "checkin": "2026-06-14",
        "checkout": "2026-05-06"
    }
}

EMPTY_FIRSTNAME_DATA = {
    **BOOKING_DATA,
    "firstname": ""
}

LONG_LASTNAME_DATA = {
    **BOOKING_DATA,
    "lastname": "A" * 1000
}

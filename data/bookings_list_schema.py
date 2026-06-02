BOOKINGS_LIST_SCHEMA = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "bookingid": {"type": "integer"}
        },
        "required": ["bookingid"]
    }
}

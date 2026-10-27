from enum import StrEnum


class Route(StrEnum):
    REGISTER = "/register"
    LOGIN = "/login"
    USERS = "/users"
    ROOMS = "/rooms"
    BOOKINGS = "/bookings"
    HEALTH = "/health"
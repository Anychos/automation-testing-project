from datetime import date, datetime, time, timedelta
from uuid import uuid4
from zoneinfo import ZoneInfo

from faker import Faker
from pydantic import EmailStr


class DataGenerator:
    def __init__(self, faker: Faker) -> None:
        self.faker = faker

    def email(self) -> EmailStr:
        return self.faker.email()

    def password(self) -> str:
        return self.faker.password()

    def room_name(self) -> str:
        return f"Автотест комната {uuid4().hex}"

    def room_capacity(self) -> int:
        return self.faker.random_int(min=2, max=10)

    def room_price(self) -> int:
        return self.faker.random_int(min=10000, max=200000)

    def booking_name(self) -> str:
        return "Автотест бронирование " + str(self.faker.random_int())

    def booking_duration(self) -> int:
        durations = [30, 60, 90, 120]
        return self.faker.random_element(elements=durations)

    def booking_date(self) -> date:
        today = datetime.now(ZoneInfo("Europe/Moscow")).date()
        available_dates = [
            today + timedelta(days=days_ahead)
            for days_ahead in range(1, 15)
            if (today + timedelta(days=days_ahead)).weekday() < 5
        ]
        return self.faker.random_element(elements=available_dates)

    def booking_start_time(self, duration_minutes: int) -> time:
        if duration_minutes not in (30, 60, 90, 120):
            raise ValueError("Invalid booking duration")

        opening_minutes = 9 * 60
        closing_minutes = 21 * 60

        available_starts = [
            time(hour=minutes // 60, minute=minutes % 60)
            for minutes in range(opening_minutes, closing_minutes, 30)
            if minutes + duration_minutes <= closing_minutes
        ]

        return self.faker.random_element(elements=available_starts)

    def booking_end_time(
        self,
        start_time: time,
        duration_minutes: int,
    ) -> time:
        if duration_minutes not in (30, 60, 90, 120):
            raise ValueError("Invalid booking duration")

        start_minutes = start_time.hour * 60 + start_time.minute
        end_minutes = start_minutes + duration_minutes

        if (
            start_time.second != 0
            or start_time.microsecond != 0
            or start_minutes < 9 * 60
            or start_minutes > 20 * 60 + 30
            or start_minutes % 30 != 0
            or end_minutes > 21 * 60
        ):
            raise ValueError("Invalid booking time")

        return time(
            hour=end_minutes // 60,
            minute=end_minutes % 60,
        )

    def booking_attendees(self, room_capacity: int) -> int:
        if room_capacity < 1:
            raise ValueError("Room capacity must be positive")

        return self.faker.random_int(
            min=1,
            max=room_capacity,
        )


fake = DataGenerator(faker=Faker())

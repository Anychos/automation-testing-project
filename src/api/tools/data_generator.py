from pydantic import EmailStr
from faker import Faker


class DataGenerator:
    def __init__(self, faker: Faker) -> None:
        self.faker = faker

    def email(self) -> EmailStr:
        return self.faker.email()

    def password(self) -> str:
        return self.faker.password()


fake = DataGenerator(faker=Faker())
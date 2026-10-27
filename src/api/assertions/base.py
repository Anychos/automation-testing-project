from typing import Any


def assert_field_value(expected: Any, actual: Any, field_name: str) -> None:
    assert expected == actual, f"Значение в поле '{field_name}' не соответсвует ожидаемому. Получено '{actual}', ожидалось '{expected}'"

def assert_status_code(expected: int, actual: int) -> None:
    assert expected == actual, f"Статус код ответа не соответсвует ожидаемому. Получен '{actual}', ожидался '{expected}'"
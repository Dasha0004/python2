import pytest

from src.decorators import log


def test_log_decorator_success(caplog):
    """Проверяет логирование при успешном выполнении функции."""

    @log()
    def add(a, b):
        return a + b

    with caplog.at_level("INFO"):
        result = add(2, 3)

    assert result == 5
    assert any("Начало выполнения функции 'add'" in msg for msg in caplog.messages)
    assert any("Функция 'add' завершена успешно с результатом: 5" in msg for msg in caplog.messages)
    assert any("Конец выполнения функции 'add'" in msg for msg in caplog.messages)


def test_log_decorator_exception(caplog):
    """Проверяет логирование при возникновении исключения в функции."""

    @log()
    def div(a, b):
        return a / b

    with caplog.at_level("INFO"), pytest.raises(ZeroDivisionError):
        div(1, 0)

    assert any("Начало выполнения функции 'div'" in msg for msg in caplog.messages)
    assert any(
        "Функция 'div' вызвала исключение ZeroDivisionError с параметрами args=(1, 0), kwargs={}" in msg
        for msg in caplog.messages
    )
    assert any("Конец выполнения функции 'div'" in msg for msg in caplog.messages)

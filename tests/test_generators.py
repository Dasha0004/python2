import sys

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions

sys.path.append(r"/Пользователи/admin/PyCharmProject/pythonProject2/src")


def test_filter_by_currency_basic():
    transactions = [
        {"id": 1, "amount": 100, "currency": "USD"},
        {"id": 2, "amount": 200, "currency": "EUR"},
        {"id": 3, "amount": 300, "currency": "USD"},
    ]
    result = list(filter_by_currency(transactions, "USD"))
    expected = [
        {"id": 1, "amount": 100, "currency": "USD"},
        {"id": 3, "amount": 300, "currency": "USD"},
    ]
    assert result == expected


def test_filter_by_currency_no_matches():
    transactions = [
        {"id": 1, "amount": 100, "currency": "USD"},
        {"id": 2, "amount": 200, "currency": "EUR"},
    ]
    result = list(filter_by_currency(transactions, "GBP"))
    assert result == []


def test_filter_by_currency_empty_list():
    transactions = []
    result = list(filter_by_currency(transactions, "USD"))
    assert result == []


def test_filter_by_currency_no_currency_key():
    transactions = [
        {"id": 1, "amount": 100},  # отсутствует currency
        {"id": 2, "amount": 200, "currency": "EUR"},
    ]
    result = list(filter_by_currency(transactions, "EUR"))
    expected = [
        {"id": 2, "amount": 200, "currency": "EUR"},
    ]
    assert result == expected


def test_transaction_descriptions_normal():
    transactions = [
        {"amount": 100, "currency": "USD"},
        {"amount": 250, "currency": "EUR"},
        {"amount": 50, "currency": "RUB"},
    ]
    expected = [
        "Транзакция на сумму 100 USD",
        "Транзакция на сумму 250 EUR",
        "Транзакция на сумму 50 RUB",
    ]
    result = list(transaction_descriptions(transactions))
    assert result == expected


def test_transaction_descriptions_empty_list():
    transactions = []
    result = list(transaction_descriptions(transactions))
    assert result == []


def test_transaction_descriptions_missing_keys():
    transactions = [
        {"amount": 100},  # нет currency
        {"currency": "EUR"},  # нет amount
        {},  # нет и amount, и currency
    ]
    expected = [
        "Транзакция на сумму 100 unknown currency",
        "Транзакция на сумму unknown amount EUR",
        "Транзакция на сумму unknown amount unknown currency",
    ]
    result = list(transaction_descriptions(transactions))
    assert result == expected

    def test_card_number_generator_basic():
        start = "0000000000000001"
        end = "0000000000000003"
        expected = [
            "0000 0000 0000 0001",
            "0000 0000 0000 0002",
            "0000 0000 0000 0003",
        ]
        result = list(card_number_generator(start, end))
        assert result == expected

    def test_card_number_generator_formatting():
        start = "1234567890123456"
        end = "1234567890123456"
        result = list(card_number_generator(start, end))
        expected = ["1234 5678 9012 3456"]
        assert result == expected
        # Проверка длины и пробелов
        for num in result:
            assert len(num) == 19  # 16 цифр + 3 пробела
            parts = num.split(" ")
            assert len(parts) == 4
            assert all(len(part) == 4 for part in parts)

    def test_card_number_generator_single_value():
        start = "0000000000000000"
        end = "0000000000000000"
        result = list(card_number_generator(start, end))
        expected = ["0000 0000 0000 0000"]
        assert result == expected

    def test_card_number_generator_full_range_small():
        # Проверка, что генерация идет от start до end включительно
        start = "0000000000000008"
        end = "0000000000000010"
        expected = [
            "0000 0000 0000 0008",
            "0000 0000 0000 0009",
            "0000 0000 0000 0010",
        ]
        result = list(card_number_generator(start, end))
        assert result == expected

    def test_card_number_generator_empty_range():
        # Если start > end, генератор не должен выдавать элементов
        start = "0000000000000010"
        end = "0000000000000005"
        result = list(card_number_generator(start, end))
        assert result == []

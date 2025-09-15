import pytest
from masks import get_mask_card_number

def test_mask_correct_card_number():
    card = "1234567890123456"
    expected = "1234 56** **** 3456"
    assert get_mask_card_number(card) == expected

def test_mask_card_with_spaces_and_symbols():
    card = "1234 56-7890 1234 56"
    expected = "1234 56** **** 3456"
    assert get_mask_card_number(card) == expected

def test_mask_short_card_number():
    card = "1234567890123"
    assert get_mask_card_number(card) == "Неверный номер карты"

def test_mask_empty_string():
    assert get_mask_card_number("") == "Неверный номер карты"

def test_mask_string_without_digits():
    assert get_mask_card_number("abcd-efgh-ijkl-mnop") == "Неверный номер карты"

def test_mask_exactly_16_digits_with_extra_chars():
    card = "12 34-56 78 90 12 34 56"
    expected = "1234 56** **** 3456"
    assert get_mask_card_number(card) == expected

def test_mask_more_than_16_digits():
    # функция берет только первые 16 цифр, лишние игнорируются
    card = "12345678901234567890"
    expected = "1234 56** **** 7890"
    assert get_mask_card_number(card) == expected

import pytest
from masks import get_mask_account

def test_mask_account_normal():
    # Проверяем корректную маску для стандартного номера счета
    account = "73654108430135874305"
    expected = "**4305"
    assert get_mask_account(account) == expected

def test_mask_account_with_non_digits():
    # Номер счета содержит пробелы и другие символы — игнорируются
    account = "7365 4108-4301_3587 4305"
    expected = "**4305"
    assert get_mask_account(account) == expected

def test_mask_account_short_number():
    # Слишком короткий номер — возвращается ошибка
    short_account = "123"
    assert get_mask_account(short_account) == "Неверный номер счета"

def test_mask_account_exactly_4_digits():
    # Равно 4 цифрам — тоже ошибка согласно функции
    account_4 = "5678"
    assert get_mask_account(account_4) == "Неверный номер счета"

def test_mask_account_empty():
    # Пустая строка => ошибка
    assert get_mask_account("") == "Неверный номер счета"

def test_mask_account_non_digit_characters_only():
    # Строка из одних букв и спецсимволов — ошибка
    assert get_mask_account("abcd-!@#") == "Неверный номер счета"
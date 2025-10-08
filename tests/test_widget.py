import sys

import pytest

from src.widget import mask_account_card

sys.path.append(r"/Пользователи/admin/PyCharmProject/pythonProject2/src")


@pytest.mark.parametrize(
    "input_str, expected_end, expected_error",
    [
        ("Visa Platinum 7000792289606361", "6361", None),
        ("Счет 1234-1234", "1234", None),
        ("Счет с номером 987654321", "4321", None),
        ("Visa Platinum Неверный номер карты", None, "Неверный номер карты"),
    ],
)
def test_mask_account_card_parametrized(input_str, expected_end, expected_error):
    result = mask_account_card(input_str)
    if expected_error:
        assert expected_error in result
    else:
        assert result.endswith(expected_end)


def test_mask_account_card_no_number():
    with pytest.raises((IndexError, ValueError)):
        mask_account_card("")


def test_mask_account_card_non_digit_number():
    result = mask_account_card("Visa Platinum 1234abcd5678efgh")
    assert result.startswith("Visa Platinum")
    if "Неверный номер карты" in result:
        assert True
    else:
        assert "**5678" in result


@pytest.fixture(
    params=[
        ("Visa Platinum 7000792289606361", "6361", None),
        ("Счет 1234-1234", "1234", None),
        ("Счет с номером 987654321", "4321", None),
        ("Visa Platinum Неверный номер карты", None, "Неверный номер карты"),
    ]
)
def card_data(request):
    return request.param


@pytest.fixture
def empty_string():
    return ""


@pytest.fixture
def non_digit_number_str():
    return "Visa Platinum 1234abcd5678efgh"

import sys

sys.path.append(r"/Пользователи/admin/PyCharmProject/pythonProject2/src")
import pytest

from src.widget import mask_account_card


@pytest.mark.parametrize(
    "input_str, expected_end, expected_error",
    [
        ("Visa Platinum 7000792289606361", "6361", None),
        ("Maestro 1234567812345678", "5678", None),
        ("Счет 73654108430135874305", "4305", None),
        ("Счет 1234", None, "Неверный номер счета"),
        ("МИР 9876543210987654", "7654", None),
        ("Счет с номером 987654321", None, "Неверный номер счета"),
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
    # при отсутствии номера (или пустой строке), ловим IndexError или ValueError
    with pytest.raises((IndexError, ValueError)):
        mask_account_card("")


def test_mask_account_card_non_digit_number():
    result = mask_account_card("Visa Platinum 1234abcd5678efgh")
    assert result.startswith("Visa Platinum")
    assert "**5678" in result


import pytest
from datetime import date

@pytest.fixture
def fixture_all_states_dates():
    return [
        {"state": "NY", "date": date(2023, 1, 10), "value": 120},
        {"state": "CA", "date": date(2023, 2, 15), "value": 200},
        {"state": "TX", "date": date(2023, 3, 20), "value": 180},
        {"state": "NY", "date": date(2023, 1, 15), "value": 140},
        {"state": "CA", "date": date(2023, 4, 10), "value": 210},
    ]

@pytest.fixture
def fixture_single_state_multiple_dates():
    return [
        {"state": "NY", "date": date(2023, 1, 10), "value": 100},
        {"state": "NY", "date": date(2023, 1, 12), "value": 110},
        {"state": "NY", "date": date(2023, 1, 15), "value": 115},
    ]

@pytest.fixture
def fixture_multiple_states_single_date():
    return [
        {"state": "NY", "date": date(2023, 5, 5), "value": 130},
        {"state": "CA", "date": date(2023, 5, 5), "value": 150},
        {"state": "TX", "date": date(2023, 5, 5), "value": 140},
    ]

@pytest.fixture
def fixture_empty_list():
    return []

@pytest.fixture
def fixture_edge_case_dates():
    return [
        {"state": "NY", "date": date(2020, 2, 29), "value": 90},  # високосный год
        {"state": "CA", "date": date(2021, 12, 31), "value": 200},
        {"state": "TX", "date": date(2022, 1, 1), "value": 210},
    ]

@pytest.mark.parametrize("test_data", [
    pytest.param("fixture_all_states_dates", id="all states multiple dates"),
    pytest.param("fixture_single_state_multiple_dates", id="single state multiple dates"),
    pytest.param("fixture_multiple_states_single_date", id="multiple states single date"),
    pytest.param("fixture_empty_list", id="empty list"),
    pytest.param("fixture_edge_case_dates", id="edge case dates"),
])
def test_function(test_data, request):
    data = request.getfixturevalue(test_data)
    result = test_mask_account_card_parametrized(data)
    assert result is not None
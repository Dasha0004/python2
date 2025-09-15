import pytest
from src.widget import mask_account_card

@pytest.mark.parametrize("input_str, expected_start", [
    ("Visa Platinum 7000792289606361", "Visa Platinum **6361"),
    ("Maestro 1234567812345678", "Maestro **5678"),
    ("Счет 73654108430135874305", "Счет **4305"),
    ("Счет 1234", "Счет Неверный номер счета"),  # короткий номер счета
    ("МИР 9876543210987654", "МИР **7654"),
    ("Счет с номером 987654321", "Счет с номером Неверный номер счета"),  # если "Счет с номером" воспринимается как тип карты — нужно проверить
])
def test_mask_account_card_parametrized(input_str, expected_start):
    result = mask_account_card(input_str)
    assert result.startswith(expected_start[:-4])  # Проверяем тип правильно распознался
    assert expected_start in result

def test_mask_account_card_incorrect_format():
    # Нет номера в строке
    with pytest.raises(IndexError):
        mask_account_card("Visa Platinum")

def test_mask_account_card_empty_string():
    with pytest.raises(IndexError):
        mask_account_card("")

def test_mask_account_card_non_digit_number():
    # В номере есть буквы — должны корректно обработать
    result = mask_account_card("Visa Platinum 1234abcd5678efgh")
    assert result.startswith("Visa Platinum **5678")



    import pytest
    from src.widget import get_date

    def test_get_date_standard():
        assert get_date("2024-03-11T02:26:18.671407") == "11.03.2024"

    def test_get_date_edge():
        assert get_date("2024-01-01T00:00:00") == "01.01.2024"
        assert get_date("2024-12-31T23:59:59") == "31.12.2024"

    def test_get_date_without_time():
        with pytest.raises(Exception):
            get_date("2024-03-11")  # или проверка на возвращаемое значение, если функция доработана

    def test_get_date_invalid():
        with pytest.raises(Exception):
            get_date("foobar")
        with pytest.raises(Exception):
            get_date("")
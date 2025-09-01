
from masks import get_mask_account, get_mask_card_number


def mask_account_card(info: str) -> str:
    """
    Принимает строку с типом и номером карты или счета, например:
    "Visa Platinum 7000792289606361", "Maestro 7000792289606361", "Счет 73654108430135874305"
    Возвращает строку с замаскированным номером, используя разные маски для карт и счетов.
    """
    parts = info.split()
    number = parts[-1]

    card_type = " ".join(parts[:-1])

    if card_type.lower().startswith("счет"):
        masked_number = get_mask_account(number)
    else:
        masked_number = get_mask_card_number(number)

    return f"{card_type} {masked_number}"


def get_date(date_str: str) -> str:
    """
    Принимает строку с датой в формате "2024-03-11T02:26:18.671407"
    Возвращает строку с датой в формате "ДД.ММ.ГГГГ" (например, "11.03.2024").
    """
    date_part = date_str.split("T")[0]
    year, month, day = date_part.split("-")
    return f"{day}.{month}.{year}"

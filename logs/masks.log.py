import logging

# Настройка логгера для модуля masks
logger = logging.getLogger("masks")
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler("masks.log", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)

file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)

logger.addHandler(file_handler)


def get_mask_card_number(card_number: str) -> str:
    """Маскирует номер банковской карты, оставляя открытыми первые 6 и последние 4 цифры"""
    clean_number = "".join(filter(str.isdigit, card_number))
    if len(clean_number) < 16:
        logger.error(f"Неверный номер карты: {card_number}")
        return "Неверный номер карты"

    masked_middle = "**" + "****"
    part1 = clean_number[0:4]
    part2 = clean_number[4:6]
    part3 = masked_middle[:2]
    part4 = masked_middle[2:]
    part5 = clean_number[-4:]
    masked = f"{part1} {part2}{part3} {part4} {part5}"

    logger.debug(f"Успешно замаскирован номер карты: {masked}")
    return masked


def get_mask_account(account_number: str) -> str:
    """Маскирует номер банковского счета, показывая только последние 4 цифры"""
    clean_number = "".join(filter(str.isdigit, account_number))
    if len(clean_number) <= 4:
        logger.error(f"Неверный номер счета: {account_number}")
        return "Неверный номер счета"
    masked = f"**{clean_number[-4:]}"
    logger.debug(f"Успешно замаскирован номер счета: {masked}")
    return masked


print(get_mask_card_number("7000792289606361"))
print(get_mask_account("73654108430135874305"))

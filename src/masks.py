def get_mask_card_number(card_number: str) -> str:
    """Маскирует номер банковской карты, оставляя открытыми первые 6 и последние 4 цифры"""
    clean_number = "".join(filter(str.isdigit, card_number))
    if len(clean_number) < 16:
        return "Неверный номер карты"

    masked_middle = "**" + "****"

    part1 = clean_number[0:4]
    part2 = clean_number[4:6]
    part3 = masked_middle[:2]
    part4 = masked_middle[2:]
    part5 = clean_number[-4:]
    return f"{part1} {part2}{part3} {part4} {part5}"

def get_mask_account(account_number: str) -> str:
    """Маскирует номер банковского счета, показывая только последние 4 цифры"""
    clean_number = "".join(filter(str.isdigit, account_number))
    if len(clean_number) <= 4:
        return "Неверный номер счета"
    return f"**{clean_number[-4:]}"

print(get_mask_card_number("7000792289606361"))
print(get_mask_account("73654108430135874305"))
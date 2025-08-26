def mask_account_card(info: str) -> str :
    parts = info.split()
    number = parts[-1]
    card_type = " ".join(parts[:-1])

    if card_type.lower().startswith("счет"):
        masked_number = mask_account(number)
        else:
        masked_number = mask_card(number)
        return f"{card_type} {masked_number}"






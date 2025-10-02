def filter_by_currency(transactions, currency):
    return (tx for tx in transactions if tx.get("currency") == currency)


def transaction_descriptions(transactions):
    for tx in transactions:
        amount = tx.get("amount", "unknown amount")
        currency = tx.get("currency", "unknown currency")
        description = f"Транзакция на сумму {amount} {currency}"
        yield description


def card_number_generator(start, end):
    """
    Генератор номеров банковских карт в формате XXXX XXXX XXXX XXXX
    start и end — строки с 16-значными номерами, например "0000000000000001"
    """
    start_num = int(start)
    end_num = int(end)
    for num in range(start_num, end_num + 1):
        s = str(num).zfill(16)
        formatted = " ".join(s[i : i + 4] for i in range(0, 16, 4))
        yield formatted

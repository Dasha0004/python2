import os

import requests
from dotenv import load_dotenv

load_dotenv()  # загружаем переменные окружения из .env

API_KEY = os.getenv("EXCHANGE_API_KEY")
BASE_URL = "https://api.apilayer.com/exchangerates_data/convert"


def get_conversion_rate(from_currency: str, to_currency: str = "RUB", amount: float = 1) -> float:
    headers = {"apikey": API_KEY}
    params = {"from": from_currency, "to": to_currency, "amount": amount}
    response = requests.get(BASE_URL, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()
    return float(data["result"])


def get_transaction_amount_rub(transaction: dict) -> float:
    """
    Принимает транзакцию с вложенной структурой.
    Возвращает сумму транзакции в рублях.
    """
    amount = float(transaction.get("operationAmount", {}).get("amount", 0))
    currency = transaction.get("operationAmount", {}).get("currency", {}).get("code", "RUB").upper()

    if currency == "RUB":
        return amount
    elif currency in ("USD", "EUR"):
        rate = get_conversion_rate(currency)
        return amount * rate
    else:
        raise ValueError(f"Unsupported currency: {currency}")

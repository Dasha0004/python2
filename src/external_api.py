import os

import requests
from dotenv import load_dotenv

load_dotenv()  # загружаем переменные окружения из .env

API_KEY = os.getenv("EXCHANGE_API_KEY")
BASE_URL = "https://api.apilayer.com/exchangerates_data/convert"


def get_usd_to_rub_rate() -> float:
    headers = {"apikey": API_KEY}
    params = {"base": "USD", "symbols": "RUB"}
    response = requests.get(BASE_URL, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()
    return data["rates"]["RUB"]


def get_eur_to_rub_rate() -> float:
    headers = {"apikey": API_KEY}
    params = {"base": "EUR", "symbols": "RUB"}
    response = requests.get(BASE_URL, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()
    return data["rates"]["RUB"]


def get_transaction_amount_rub(transaction: dict) -> float:
    """
    Принимает транзакцию с ключами 'amount' и 'currency'.
    Возвращает сумму транзакции в рублях.
    """
    amount = float(transaction.get("amount", 0))
    currency = transaction.get("currency", "RUB").upper()

    if currency == "RUB":
        return amount
    elif currency == "USD":
        rate = get_usd_to_rub_rate()
        return amount * rate
    elif currency == "EUR":
        rate = get_eur_to_rub_rate()
        return amount * rate
    else:
        raise ValueError(f"Unsupported currency: {currency}")

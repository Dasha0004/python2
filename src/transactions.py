import pandas as pd


def read_transactions_csv(file_path):
    """
    Считывание финансовых операций из CSV-файла.
    Возвращает список словарей с транзакциями.
    """
    df = pd.read_csv(file_path, encoding="utf-8")
    return df.to_dict(orient="records")


def read_transactions_excel(file_path):
    """
    Считывание финансовых операций из Excel-файла (XLSX).
    Возвращает список словарей с транзакциями.
    """
    df = pd.read_excel(file_path, engine="openpyxl")
    return df.to_dict(orient="records")

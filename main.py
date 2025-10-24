import csv
import json

import pandas


def read_json_file(filename: str) -> list[dict]:
    with open(filename, encoding="utf-8") as f:
        return json.load(f)


def read_csv_file(filename: str) -> list[dict]:
    with open(filename, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def read_xlsx_file(filename: str) -> list[dict]:
    wb = pandas.load_workbook(filename)
    sheet = wb.active
    keys = [cell.value for cell in next(sheet.iter_rows(min_row=1, max_row=1))]
    data = []
    for row in sheet.iter_rows(min_row=2, values_only=True):
        entry = dict(zip(keys, row))
        data.append(entry)
    return data


def filter_by_status(data: list[dict], status: str) -> list[dict]:
    status_upper = status.upper()
    return [op for op in data if op.get("status", "").upper() == status_upper]


def sort_by_date(data: list[dict], ascending=True) -> list[dict]:
    from datetime import datetime

    def parse_date(d):
        try:
            return datetime.strptime(d, "%d.%m.%Y")
        except Exception:
            return datetime.min

    return sorted(data, key=lambda x: parse_date(x.get("date", "")), reverse=not ascending)


def filter_by_currency(data: list[dict], currency: str = "руб.") -> list[dict]:
    # Проверяем поле с суммой на вхождение currency или 'руб' внутри операцции
    filtered = []
    for op in data:
        amount_str = op.get("amount", "")  # например: "40542 руб." или "130 USD"
        if currency.lower() in amount_str.lower():
            filtered.append(op)
    return filtered


def filter_by_description_word(data: list[dict], word: str) -> list[dict]:
    word_lower = word.lower()
    return [op for op in data if word_lower in op.get("description", "").lower()]


def print_operations(operations: list[dict]) -> None:
    print(f"Всего банковских операций в выборке: {len(operations)}\n")
    for op in operations:
        date = op.get("date", "")
        desc = op.get("description", "")
        from_ = op.get("from", "")
        to_ = op.get("to", "")
        amount = op.get("amount", "")
        print(f"{date} {desc}")
        if from_ and to_:
            print(f"{from_} -> {to_}")
        print(f"Сумма: {amount}\n")


def main():
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    file_choice = input().strip()
    if file_choice == "1":
        print("Для обработки выбран JSON-файл.")
        filename = input("Введите имя JSON-файла: ").strip()
        data = read_json_file(filename)
    elif file_choice == "2":
        print("Для обработки выбран CSV-файл.")
        filename = input("Введите имя CSV-файла: ").strip()
        data = read_csv_file(filename)
    elif file_choice == "3":
        print("Для обработки выбран XLSX-файл.")
        filename = input("Введите имя XLSX-файла: ").strip()
        data = read_xlsx_file(filename)
    else:
        print("Некорректный выбор.")
        return

    valid_statuses = ["EXECUTED", "CANCELED", "PENDING"]
    while True:
        print(
            "Введите статус, по которому необходимо выполнить фильтрацию. \nДоступные для фильтрации статусы: EXECUTED, CANCELED, PENDING"
        )
        status_input = input().strip().upper()
        if status_input in valid_statuses:
            print(f'Операции отфильтрованы по статусу "{status_input}"')
            filtered = filter_by_status(data, status_input)
            break
        else:
            print(f'Статус операции "{status_input}" недоступен.')

    print("Отсортировать операции по дате? Да/Нет")
    sort_answer = input().strip().lower()
    if sort_answer == "да":
        print("Отсортировать по возрастанию или по убыванию?")
        order = input().strip().lower()
        ascending = True if "возрастанию" in order else False
        filtered = sort_by_date(filtered, ascending=ascending)

    print("водить только рублевые транзакции? Да/Нет")
    only_rubles = input().strip().lower() == "да"
    if only_rubles:
        filtered = filter_by_currency(filtered, currency="руб.")

    print("Отфильтровать список транзакций по определенному слову в описании? Да/Нет")
    filter_desc = input().strip().lower()
    if filter_desc == "да":
        print("Введите слово для фильтрации в описании:")
        word = input().strip()
        filtered = filter_by_description_word(filtered, word)

    print("Распечатываю итоговый список транзакций...\n")
    if filtered:
        print_operations(filtered)
    else:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")

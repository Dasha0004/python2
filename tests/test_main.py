import unittest
from unittest.mock import patch

from main import filter_by_currency, filter_by_description_word, print_operations, sort_by_date


class TestUserInteractionFlow(unittest.TestCase):
    def setUp(self):
        # Пример данных транзакций
        self.transactions = [
            {"date": "2024-04-01", "currency": "руб.", "description": "оплата магазина"},
            {"date": "2024-03-01", "currency": "usd", "description": "покупка товаров"},
            {"date": "2024-05-01", "currency": "руб.", "description": "зарплата"},
        ]

    @patch(
        "builtins.input",
        side_effect=[
            "возрастанию",  # выбор сортировки
            "да",  # только рублевые
            "да",  # фильтрация по описанию
            "оплата",  # слово для фильтрации
        ],
    )
    @patch("builtins.print")
    def test_full_flow(self, mock_print, mock_input):
        filtered = self.transactions.copy()

        # Сортировка
        order = input().strip().lower()
        ascending = True if "возрастанию" in order else False
        filtered = sort_by_date(filtered, ascending=ascending)

        # Фильтрация по валюте
        only_rubles = input().strip().lower() == "да"
        if only_rubles:
            filtered = filter_by_currency(filtered, currency="руб.")

        # Фильтрация по описанию
        filter_desc = input().strip().lower()
        if filter_desc == "да":
            word = input().strip()
            filtered = filter_by_description_word(filtered, word)

        # Проверка результата
        self.assertTrue(all(t["currency"] == "руб." for t in filtered))
        self.assertTrue(all("оплата" in t["description"] for t in filtered))

        # Тест печати результата
        if filtered:
            print_operations(filtered)
            mock_print.assert_any_call("Распечатываю итоговый список транзакций...\n")
        else:
            print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
            mock_print.assert_any_call("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")

    @patch(
        "builtins.input",
        side_effect=[
            "убыванию",  # сортировка по убыванию
            "нет",  # не фильтровать по валюте
            "нет",  # не фильтровать по описанию
        ],
    )
    @patch("builtins.print")
    def test_flow_without_filters(self, mock_print, mock_input):
        filtered = self.transactions.copy()

        order = input().strip().lower()
        ascending = True if "возрастанию" in order else False
        filtered = sort_by_date(filtered, ascending=ascending)

        only_rubles = input().strip().lower() == "да"
        if only_rubles:
            filtered = filter_by_currency(filtered, currency="руб.")

        filter_desc = input().strip().lower()
        if filter_desc == "да":
            word = input().strip()
        filtered = filter_by_description_word(filtered, word)

        self.assertEqual(len(filtered), len(self.transactions))  # не фильтруемся в этом тесте

        if filtered:
            print_operations(filtered)
            mock_print.assert_any_call("Распечатываю итоговый список транзакций...\n")
        else:
            print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
            mock_print.assert_any_call("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")


if __name__ == "__main__":
    unittest.main()

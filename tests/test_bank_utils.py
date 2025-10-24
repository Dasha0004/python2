import unittest

from src.bank_utils import process_bank_operations, process_bank_search


class TestProcessBankSearch(unittest.TestCase):
    def setUp(self):
        self.data = [
            {"description": "Оплата заказа в магазине"},
            {"description": "Пополнение счета"},
            {"description": "Снятие наличных в банкомате"},
            {"description": "Перевод средств"},
            {"description": "оплата услуг интернета"},
            {"other_key": "нет описания"},
            {"description": "Оплата аренды дома"},
        ]

    def test_search_simple_word(self):
        result = process_bank_search(self.data, "оплата")
        expected = [
            {"description": "Оплата заказа в магазине"},
            {"description": "оплата услуг интернета"},
            {"description": "Оплата аренды дома"},
        ]
        self.assertEqual(result, expected)

    def test_search_case_insensitive(self):
        result = process_bank_search(self.data, "ПОПОЛНЕНИЕ")
        expected = [{"description": "Пополнение счета"}]
        self.assertEqual(result, expected)

    def test_search_partial_match(self):
        result = process_bank_search(self.data, "наличн")
        expected = [{"description": "Снятие наличных в банкомате"}]
        self.assertEqual(result, expected)

    def test_search_no_matches(self):
        result = process_bank_search(self.data, "кредит")
        expected = []
        self.assertEqual(result, expected)

    def test_search_missing_description_key(self):
        result = process_bank_search(self.data, "нет")
        expected = []
        self.assertEqual(result, expected)

    def test_search_regex(self):
        # ищет слова начинающиеся на "пер" (перевод)
        result = process_bank_search(self.data, r"\bпер\w*")
        expected = [{"description": "Перевод средств"}]
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()


class TestProcessBankOperations(unittest.TestCase):
    def setUp(self):
        self.data = [
            {"description": "Оплата магазина"},
            {"description": "Пополнение счета"},
            {"description": "Снятие наличных"},
            {"description": "Оплата услуг интернета"},
            {"description": "Покупка продуктов"},
            {"description": "Оплата аренды"},
            {"description": ""},  # пустое описание
            {},  # словарь без description
        ]
        self.categories = ["оплата", "пополнение", "снятие", "перевод"]

    def test_count_operations(self):
        result = process_bank_operations(self.data, self.categories)
        expected = {
            "оплата": 3,  # совпадения в 1,4,6 элементах
            "пополнение": 1,  # совпадение во 2-ом элементе
            "снятие": 1,  # совпадение в 3-ем элементе
            "перевод": 0,  # нет совпадений
        }
        self.assertEqual(result, expected)

    def test_empty_data(self):
        result = process_bank_operations([], self.categories)
        expected = {cat: 0 for cat in self.categories}
        self.assertEqual(result, expected)

    def test_empty_categories(self):
        result = process_bank_operations(self.data, [])
        self.assertEqual(result, {})

    def test_case_insensitivity(self):
        data = [{"description": "ОПЛАТА услуг"}, {"description": "оплата счетов"}]
        categories = ["Оплата"]
        result = process_bank_operations(data, categories)
        self.assertEqual(result, {"Оплата": 2})


if __name__ == "__main__":
    unittest.main()

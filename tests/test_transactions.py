import unittest
from unittest.mock import MagicMock, patch

import pandas as pd

from src.transactions import read_transactions_csv, read_transactions_excel


class TestReadTransactions(unittest.TestCase):
    @patch("src.transactions.pd.read_csv")
    def test_read_transactions_csv(self, mock_read_csv):
        # Заготовка данных - DataFrame
        data = {"date": ["2024-01-01"], "amount": [100], "description": ["test"]}
        df = pd.DataFrame(data)

        # Настраиваем mock возвращать наш DataFrame
        mock_read_csv.return_value = df

        # Вызываем функцию
        result = read_transactions_csv("fake_path.csv")

        # Проверка, что pd.read_csv вызван с нужным аргументом и encoding
        mock_read_csv.assert_called_once_with("fake_path.csv", encoding="utf-8")

        # Проверка результата - список словарей
        expected = df.to_dict(orient="records")
        self.assertEqual(result, expected)

    @patch("src.transactions.pd.read_excel")
    def test_read_transactions_excel(self, mock_read_excel):
        # Заготовка данных - DataFrame
        data = {"date": ["2024-02-01"], "amount": [200], "description": ["test excel"]}
        df = pd.DataFrame(data)

        # Настраиваем mock возвращать наш DataFrame
        mock_read_excel.return_value = df

        # Вызываем функцию
        result = read_transactions_excel("fake_path.xlsx")

        # Проверка, что pd.read_excel вызван с нужным аргументом и engine='openpyxl'
        mock_read_excel.assert_called_once_with("fake_path.xlsx", engine="openpyxl")

        # Проверка результата - список словарей
        expected = df.to_dict(orient="records")
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()

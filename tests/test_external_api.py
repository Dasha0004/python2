import unittest
from unittest.mock import Mock, patch

from src.external_api import get_conversion_rate, get_transaction_amount_rub


class TestGetTransactionAmountRub(unittest.TestCase):

    @patch("src.external_api.get_conversion_rate")
    def test_rub_currency(self, mock_get_rate):
        transaction = {"operationAmount": {"amount": "1000", "currency": {"code": "RUB"}}}
        result = get_transaction_amount_rub(transaction)
        self.assertEqual(result, 1000.0)
        mock_get_rate.assert_not_called()

    @patch("src.external_api.get_conversion_rate", return_value=70.0)
    def test_usd_currency(self, mock_get_rate):
        transaction = {"operationAmount": {"amount": "10", "currency": {"code": "USD"}}}
        result = get_transaction_amount_rub(transaction)
        self.assertEqual(result, 700.0)
        mock_get_rate.assert_called_once_with("USD")

    @patch("src.external_api.get_conversion_rate", return_value=80.0)
    def test_eur_currency(self, mock_get_rate):
        transaction = {"operationAmount": {"amount": "5", "currency": {"code": "EUR"}}}
        result = get_transaction_amount_rub(transaction)
        self.assertEqual(result, 400.0)  # 5 * 80
        mock_get_rate.assert_called_once_with("EUR")

    def test_unsupported_currency_raises(self):
        transaction = {"operationAmount": {"amount": "100", "currency": {"code": "GBP"}}}
        with self.assertRaises(ValueError) as e:
            get_transaction_amount_rub(transaction)
        self.assertIn("Unsupported currency", str(e.exception))

    def test_missing_fields_defaults(self):
        # Если в транзакции нет currency и amount, сумма 0, валюта RUB
        transaction = {}
        result = get_transaction_amount_rub(transaction)
        self.assertEqual(result, 0.0)


if __name__ == "__main__":
    unittest.main()

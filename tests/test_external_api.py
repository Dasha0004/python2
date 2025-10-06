import unittest
from unittest.mock import patch

from src.external_api import get_transaction_amount_rub


class TestGetTransactionAmountRub(unittest.TestCase):

    def test_rub_currency(self):
        transaction = {"amount": 123.45, "currency": "RUB"}
        result = get_transaction_amount_rub(transaction)
        self.assertEqual(result, 123.45)

    @patch("src.get_usd_to_rub_rate")
    def test_usd_currency(self, mock_usd_rate):
        mock_usd_rate.return_value = 70.5
        transaction = {"amount": 2, "currency": "USD"}
        result = get_transaction_amount_rub(transaction)
        self.assertEqual(result, 2 * 70.5)
        mock_usd_rate.assert_called_once()

    @patch("src.get_eur_to_rub_rate")
    def test_eur_currency(self, mock_eur_rate):
        mock_eur_rate.return_value = 80.0
        transaction = {"amount": 3.5, "currency": "EUR"}
        result = get_transaction_amount_rub(transaction)
        self.assertEqual(result, 3.5 * 80.0)
        mock_eur_rate.assert_called_once()

    def test_unsupported_currency(self):
        transaction = {"amount": 10, "currency": "GBP"}
        with self.assertRaises(ValueError) as context:
            get_transaction_amount_rub(transaction)
        self.assertIn("Unsupported currency", str(context.exception))

    def test_no_currency_key(self):
        transaction = {"amount": 50}
        result = get_transaction_amount_rub(transaction)
        self.assertEqual(result, 50)

    def test_amount_missing_defaults_to_zero(self):
        transaction = {"currency": "RUB"}
        result = get_transaction_amount_rub(transaction)
        self.assertEqual(result, 0)


if __name__ == "__main__":
    unittest.main()

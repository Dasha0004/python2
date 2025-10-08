import json
import unittest
from unittest.mock import mock_open, patch

from src.utils import load_transactions


class TestLoadTransactions(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open, read_data='[{"id": 1, "amount": 100}]')
    def test_valid_list(self, mock_file):
        result = load_transactions("dummy.json")
        self.assertEqual(result, [{"id": 1, "amount": 100}])
        mock_file.assert_called_once_with("dummy.json", "r", encoding="utf-8")

    @patch("builtins.open", new_callable=mock_open, read_data='{"id": 1}')
    def test_not_a_list(self, mock_file):
        result = load_transactions("dummy.json")
        self.assertEqual(result, [])

    @patch("builtins.open")
    def test_file_not_found(self, mock_file):
        mock_file.side_effect = FileNotFoundError
        result = load_transactions("dummy.json")
        self.assertEqual(result, [])

    @patch("builtins.open", new_callable=mock_open, read_data="invalid json")
    @patch("json.load", side_effect=json.JSONDecodeError("Expecting value", "doc", 0))
    def test_json_decode_error(self, mock_json_load, mock_file):
        result = load_transactions("dummy.json")
        self.assertEqual(result, [])

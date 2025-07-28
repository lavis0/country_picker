import json
import unittest
from unittest.mock import Mock
from PyQt6.QtCore import QByteArray
from src.country_picker.gui import DataWorker


class TestDataWorker(unittest.TestCase):
    """Test cases for DataWorker JSON parsing logic."""

    def test_handle_data_with_common_names(self):
        """Test parsing JSON with a 'common' name structure."""
        worker = DataWorker()
        worker.resultReady = Mock()
        worker.errorOccurred = Mock()

        test_data = [
            {"name": {"common": "United States"}},
            {"name": {"common": "Canada"}},
            {"name": {"common": "Mexico"}}
        ]
        json_bytes = QByteArray(json.dumps(test_data).encode('utf-8'))

        worker._handle_data(json_bytes)

        worker.resultReady.emit.assert_called_once()
        emitted_countries = worker.resultReady.emit.call_args[0][0]
        self.assertEqual(emitted_countries, ["Canada", "Mexico", "United States"])

    def test_handle_data_with_string_names(self):
        """Test parsing JSON with string name structure."""
        worker = DataWorker()
        worker.resultReady = Mock()
        worker.errorOccurred = Mock()

        test_data = [
            {"name": "Brazil"},
            {"name": "Argentina"},
            {"name": "Chile"}
        ]
        json_bytes = QByteArray(json.dumps(test_data).encode('utf-8'))

        worker._handle_data(json_bytes)

        worker.resultReady.emit.assert_called_once()
        emitted_countries = worker.resultReady.emit.call_args[0][0]
        self.assertEqual(emitted_countries, ["Argentina", "Brazil", "Chile"])

    def test_handle_data_mixed_formats(self):
        """Test parsing JSON with mixed name formats."""
        worker = DataWorker()
        worker.resultReady = Mock()
        worker.errorOccurred = Mock()

        test_data = [
            {"name": {"common": "France"}},
            {"name": "Germany"},
            {"name": {"common": "Italy"}},
            {"name": "Spain"}
        ]
        json_bytes = QByteArray(json.dumps(test_data).encode('utf-8'))

        worker._handle_data(json_bytes)

        worker.resultReady.emit.assert_called_once()
        emitted_countries = worker.resultReady.emit.call_args[0][0]
        self.assertEqual(emitted_countries, ["France", "Germany", "Italy", "Spain"])

    def test_handle_data_invalid_json(self):
        """Test handling of invalid JSON data."""
        worker = DataWorker()
        worker.resultReady = Mock()
        worker.errorOccurred = Mock()

        # Invalid JSON
        invalid_json = QByteArray(b"invalid json data")

        worker._handle_data(invalid_json)

        worker.errorOccurred.emit.assert_called_once()
        worker.resultReady.emit.assert_not_called()

    def test_handle_data_empty_list(self):
        """Test parsing empty country list."""
        worker = DataWorker()
        worker.resultReady = Mock()
        worker.errorOccurred = Mock()

        test_data = []
        json_bytes = QByteArray(json.dumps(test_data).encode('utf-8'))

        worker._handle_data(json_bytes)

        worker.resultReady.emit.assert_called_once()
        emitted_countries = worker.resultReady.emit.call_args[0][0]
        self.assertEqual(emitted_countries, [])

    def test_handle_data_filters_invalid_entries(self):
        """Test that invalid entries are filtered out."""
        worker = DataWorker()
        worker.resultReady = Mock()
        worker.errorOccurred = Mock()

        # Data with some invalid entries
        test_data = [
            {"name": {"common": "Valid Country"}},
            {"name": {"common": None}},  # Invalid - None value
            {"name": {"official": "No Common"}},  # Invalid - no common field
            {"name": 123},  # Invalid - not string or dict
            {"other_field": "No Name"}  # Invalid - no name field
        ]
        json_bytes = QByteArray(json.dumps(test_data).encode('utf-8'))

        worker._handle_data(json_bytes)

        worker.resultReady.emit.assert_called_once()
        emitted_countries = worker.resultReady.emit.call_args[0][0]
        self.assertEqual(emitted_countries, ["Valid Country"])


if __name__ == '__main__':
    unittest.main()

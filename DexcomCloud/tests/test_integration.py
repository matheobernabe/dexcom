import pytest
from unittest.mock import MagicMock, patch
from DataProcessor.publisher import Publisher
from main import fetch_and_publish

@patch("requests.get")
def test_fetch_and_publish(mock_get):
    mock_publisher = MagicMock()
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"glucose": 120}

    fetch_and_publish(mock_publisher)
    mock_publisher.send_event_to_kafka.assert_called_once_with({"glucose": 120})

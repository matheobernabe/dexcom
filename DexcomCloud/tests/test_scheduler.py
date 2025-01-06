import pytest
from unittest.mock import MagicMock, patch
from DataProcessor.scheduler import Scheduler

def test_scheduler_initialization():
    mock_publisher = MagicMock()
    scheduler = Scheduler(publisher=mock_publisher, fetch_url="http://test-url.com", interval=5)
    assert scheduler.fetch_url == "http://test-url.com"
    assert scheduler.interval == 5

@patch("requests.get")
def test_fetch_and_emit_success(mock_get):
    mock_publisher = MagicMock()
    scheduler = Scheduler(publisher=mock_publisher, fetch_url="http://test-url.com", interval=5)

    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"glucose": 120}

    scheduler.fetch_and_emit()
    mock_publisher.emit_event.assert_called_once_with("glucose_update", {"glucose": 120})

@patch('requests.get')
def test_fetch_and_emit_failure(mock_fetch_data):
    mock_fetch_data.side_effect = Exception("Connection Error")
    scheduler = Scheduler()
    with pytest.raises(Exception, match="Connection Error"):
        scheduler.fetch_and_emit()


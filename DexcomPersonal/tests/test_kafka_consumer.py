import pytest
from unittest.mock import Mock, patch
from datetime import datetime
from DexcomPersonal.kafka_consumer import GlucoseConsumer

class TestGlucoseConsumer:
    @pytest.fixture
    def mock_data_manager(self):
        return Mock()

    @pytest.fixture
    def mock_alert_manager(self):
        return Mock()

    @pytest.fixture
    def consumer(self, mock_data_manager, mock_alert_manager):
        with patch('kafka.KafkaConsumer'):
            return GlucoseConsumer(mock_data_manager, mock_alert_manager)

    def test_handle_glucose_measurement(self, consumer, mock_data_manager):
        data = {
            'timestamp': datetime.now().isoformat(),
            'glucose_level': 120
        }
        consumer._handle_glucose_measurement(data)
        mock_data_manager.add_glucose_reading.assert_called_once()

    def test_handle_glucose_alert(self, consumer, mock_alert_manager):
        alert = {
            'type': 'HYPOGLYCEMIA',
            'glucose_level': 65
        }
        consumer._handle_glucose_alert(alert)
        mock_alert_manager.process_alert.assert_called_once_with(alert)
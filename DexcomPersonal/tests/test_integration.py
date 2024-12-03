import pytest
from unittest.mock import Mock, patch
from datetime import datetime
from DexcomPersonal.insulin_manager import InsulinManager
from DexcomPersonal.data_manager import DataManager
from DexcomPersonal.kafka_consumer import GlucoseConsumer
from DexcomPersonal.alert_manager import AlertManager

class TestDexcomPersonalIntegration:
    @pytest.fixture
    def setup_components(self, tmp_path):
        # Créer les composants avec une DB temporaire
        db_path = tmp_path / "test.db"
        data_manager = DataManager(str(db_path))
        
        # Mock les composants externes
        insulin_pump = Mock()
        cloud_sync = Mock()
        alert_manager = AlertManager()
        
        # Mock Kafka Consumer
        mock_kafka_consumer = Mock()
        with patch('kafka.KafkaConsumer', return_value=mock_kafka_consumer):
            glucose_consumer = GlucoseConsumer(data_manager, alert_manager)
            glucose_consumer.consumer = mock_kafka_consumer
        
        # Créer le gestionnaire d'insuline
        insulin_manager = InsulinManager(insulin_pump, data_manager, cloud_sync)
        
        return data_manager, insulin_manager, glucose_consumer, alert_manager, cloud_sync

    def test_complete_data_flow(self, setup_components):
        data_manager, insulin_manager, glucose_consumer, alert_manager, cloud_sync = setup_components
        
        # Simuler une lecture de glucose
        glucose_data = {
            'timestamp': datetime.now().isoformat(),
            'glucose_level': 65.0,
            'unit': 'mg/dL'
        }
        glucose_consumer._handle_glucose_measurement(glucose_data)
        
        # Vérifier le stockage
        history = data_manager.get_glucose_history(hours=1)
        assert len(history) == 1
        
        # Simuler un bolus
        insulin_manager.deliver_bolus(1.0)
        
        # Vérifier la sync
        assert cloud_sync.sync_insulin_data.called or cloud_sync.sync_glucose_data.called
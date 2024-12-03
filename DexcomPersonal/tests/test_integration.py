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
        
        # Créer les gestionnaires
        insulin_manager = InsulinManager(insulin_pump, data_manager, cloud_sync)
        glucose_consumer = GlucoseConsumer(data_manager, alert_manager)
        
        return data_manager, insulin_manager, glucose_consumer, alert_manager, cloud_sync

    def test_glucose_insulin_workflow(self, setup_components):
        data_manager, insulin_manager, glucose_consumer, _, cloud_sync = setup_components
        
        # Simuler la réception d'une donnée de glucose via Kafka
        glucose_data = {
            'timestamp': datetime.now().isoformat(),
            'glucose_level': 180.0,
            'unit': 'mg/dL'
        }
        glucose_consumer._handle_glucose_measurement(glucose_data)
        
        # Vérifier que les données sont bien enregistrées
        history = data_manager.get_glucose_history(hours=1)
        assert len(history) == 1
        assert history.iloc[0]['glucose_level'] == 180.0
        
        # Simuler un bolus d'insuline
        insulin_manager.deliver_bolus(2.0)
        
        # Vérifier l'historique d'insuline
        insulin_history = data_manager.get_insulin_history(hours=1)
        assert len(insulin_history) == 1
        assert insulin_history.iloc[0]['units'] == 2.0
        
        # Vérifier la synchronisation cloud
        assert cloud_sync.sync_insulin_data.called

    def test_alert_workflow(self, setup_components, capsys):
        _, _, glucose_consumer, alert_manager, _ = setup_components
        
        # Test pour hypoglycémie
        hypo_data = {
            'type': 'HYPOGLYCEMIA',
            'glucose_level': 65,
            'timestamp': datetime.now().isoformat()
        }
        glucose_consumer._handle_glucose_alert(hypo_data)
        captured = capsys.readouterr()
        assert "URGENCE Hypoglycémie" in captured.out
        
        # Test pour hyperglycémie
        hyper_data = {
            'type': 'HYPERGLYCEMIA',
            'glucose_level': 185,
            'timestamp': datetime.now().isoformat()
        }
        glucose_consumer._handle_glucose_alert(hyper_data)
        captured = capsys.readouterr()
        assert "Attention Hyperglycémie" in captured.out

    def test_complete_data_flow(self, setup_components):
        data_manager, insulin_manager, glucose_consumer, alert_manager, cloud_sync = setup_components
        
        # 1. Réception données glucose
        glucose_data = {
            'timestamp': datetime.now().isoformat(),
            'glucose_level': 65.0,
            'unit': 'mg/dL'
        }
        glucose_consumer._handle_glucose_measurement(glucose_data)
        
        # 2. Vérifier stockage données
        history = data_manager.get_glucose_history(hours=1)
        assert len(history) == 1
        
        # 3. Simuler correction avec insuline
        insulin_manager.deliver_bolus(1.0)
        
        # 4. Vérifier synchronisation
        assert cloud_sync.sync_glucose_data.called or cloud_sync.sync_insulin_data.called
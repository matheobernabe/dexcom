import pytest
from unittest.mock import patch
from datetime import datetime
from DexcomPersonal.alert_manager import AlertManager

class TestAlertManager:
    @pytest.fixture
    def alert_manager(self):
        return AlertManager()

    @pytest.fixture
    def sample_hypo_alert(self):
        return {
            'type': 'HYPOGLYCEMIA',
            'glucose_level': 65,
            'timestamp': datetime.now().isoformat()
        }

    def test_sound_alerts(self, alert_manager, sample_hypo_alert):
        """Test de la gestion des alertes sonores"""
        # Test avec son activé
        alert_manager.update_settings({'sound_enabled': True})
        with patch.object(alert_manager, '_notify') as mock_notify:
            alert_manager.process_alert(sample_hypo_alert)
            mock_notify.assert_called_with(
                "URGENCE Hypoglycémie",
                f"Glucose: {sample_hypo_alert['glucose_level']} mg/dL",
                urgent=True
            )
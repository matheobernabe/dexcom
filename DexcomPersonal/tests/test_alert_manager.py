import pytest
from datetime import datetime
from DexcomPersonal.old.alert_manager import AlertManager

class TestAlertManager:
    @pytest.fixture
    def alert_manager(self):
        """Fixture de base pour l'AlertManager"""
        return AlertManager()

    @pytest.fixture
    def sample_hypo_alert(self):
        """Fixture pour une alerte d'hypoglycémie"""
        return {
            'type': 'HYPOGLYCEMIA',
            'glucose_level': 65,
            'timestamp': datetime.now().isoformat()
        }

    @pytest.fixture
    def sample_hyper_alert(self):
        """Fixture pour une alerte d'hyperglycémie"""
        return {
            'type': 'HYPERGLYCEMIA',
            'glucose_level': 185,
            'timestamp': datetime.now().isoformat()
        }

    def test_initial_settings(self, alert_manager):
        """Test des paramètres initiaux"""
        assert alert_manager.alert_settings['hypo_threshold'] == 70
        assert alert_manager.alert_settings['hyper_threshold'] == 180
        assert alert_manager.alert_settings['rate_of_change_threshold'] == 2
        assert alert_manager.alert_settings['notification_enabled'] is True
        assert alert_manager.alert_settings['sound_enabled'] is True

    def test_update_settings(self, alert_manager):
        """Test de la mise à jour des paramètres"""
        new_settings = {
            'hypo_threshold': 75,
            'hyper_threshold': 170,
            'sound_enabled': False
        }
        alert_manager.update_settings(new_settings)
        
        assert alert_manager.alert_settings['hypo_threshold'] == 75
        assert alert_manager.alert_settings['hyper_threshold'] == 170
        assert alert_manager.alert_settings['sound_enabled'] is False
        # Vérifie que les autres paramètres n'ont pas changé
        assert alert_manager.alert_settings['rate_of_change_threshold'] == 2
        assert alert_manager.alert_settings['notification_enabled'] is True

    def test_should_process_hypo_alert(self, alert_manager, sample_hypo_alert):
        """Test de la décision de traitement pour une hypo"""
        # Cas où l'alerte devrait être traitée
        assert alert_manager._should_process_alert(sample_hypo_alert) is True
        
        # Cas où le niveau est au-dessus du seuil
        sample_hypo_alert['glucose_level'] = 75
        assert alert_manager._should_process_alert(sample_hypo_alert) is False

    def test_should_process_hyper_alert(self, alert_manager, sample_hyper_alert):
        """Test de la décision de traitement pour une hyper"""
        # Cas où l'alerte devrait être traitée
        assert alert_manager._should_process_alert(sample_hyper_alert) is True
        
        # Cas où le niveau est en-dessous du seuil
        sample_hyper_alert['glucose_level'] = 175
        assert alert_manager._should_process_alert(sample_hyper_alert) is False

    def test_notifications_disabled(self, alert_manager, sample_hypo_alert):
        """Test quand les notifications sont désactivées"""
        alert_manager.update_settings({'notification_enabled': False})
        assert alert_manager._should_process_alert(sample_hypo_alert) is False

    def test_process_hypo_alert(self, alert_manager, sample_hypo_alert, capsys):
        """Test du traitement complet d'une alerte hypo"""
        alert_manager.process_alert(sample_hypo_alert)
        captured = capsys.readouterr()
        assert "URGENCE Hypoglycémie" in captured.out
        assert "65 mg/dL" in captured.out

    def test_process_hyper_alert(self, alert_manager, sample_hyper_alert, capsys):
        """Test du traitement complet d'une alerte hyper"""
        alert_manager.process_alert(sample_hyper_alert)
        captured = capsys.readouterr()
        assert "Attention Hyperglycémie" in captured.out
        assert "185 mg/dL" in captured.out

    def test_sound_alerts(self, alert_manager, sample_hypo_alert):
        """Test de la gestion des alertes sonores"""
        # Test avec son activé
        alert_manager.update_settings({'sound_enabled': True})
        with pytest.mock.patch.object(alert_manager, '_notify') as mock_notify:
            alert_manager.process_alert(sample_hypo_alert)
            mock_notify.assert_called_with(
                "URGENCE Hypoglycémie",
                "Glucose: 65 mg/dL",
                urgent=True
            )

        # Test avec son désactivé
        alert_manager.update_settings({'sound_enabled': False})
        with pytest.mock.patch.object(alert_manager, '_notify') as mock_notify:
            alert_manager.process_alert(sample_hypo_alert)
            mock_notify.assert_called_with(
                "URGENCE Hypoglycémie",
                "Glucose: 65 mg/dL",
                urgent=True
            )

    def test_invalid_alert_type(self, alert_manager, capsys):
        """Test avec un type d'alerte invalide"""
        invalid_alert = {
            'type': 'INVALID_TYPE',
            'glucose_level': 100,
            'timestamp': datetime.now().isoformat()
        }
        alert_manager.process_alert(invalid_alert)
        captured = capsys.readouterr()
        assert captured.out == ""  # Aucune notification ne devrait être émise

    def test_missing_data(self, alert_manager):
        """Test avec des données manquantes"""
        incomplete_alert = {
            'type': 'HYPOGLYCEMIA'
            # glucose_level manquant
        }
        with pytest.raises(KeyError):
            alert_manager.process_alert(incomplete_alert)
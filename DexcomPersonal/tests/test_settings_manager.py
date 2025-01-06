import pytest
import json
from datetime import time
from unittest.mock import mock_open, patch
from DexcomPersonal.old.user_settings import SettingsManager, UserSettings

class TestSettingsManager:
    @pytest.fixture
    def settings_manager(self):
        return SettingsManager("test_settings.json")

    def test_load_default_settings(self):
        with patch('builtins.open', mock_open()) as mock_file:
            mock_file.side_effect = FileNotFoundError
            manager = SettingsManager()
            assert isinstance(manager.settings, UserSettings)
            assert manager.settings.hypo_threshold == 70.0

    def test_save_settings(self, settings_manager):
        with patch('builtins.open', mock_open()) as mock_file:
            assert settings_manager.save_settings() is True

    def test_update_settings(self, settings_manager):
        new_settings = {
            'hypo_threshold': 75.0,
            'hyper_threshold': 170.0
        }
        assert settings_manager.update_settings(new_settings) is True
        assert settings_manager.settings.hypo_threshold == 75.0
        assert settings_manager.settings.hyper_threshold == 170.0

    def test_validate_settings(self, settings_manager):
        # Test paramètres valides
        assert settings_manager.validate_settings() is True
        
        # Test paramètres invalides
        settings_manager.settings.hypo_threshold = 30.0
        assert settings_manager.validate_settings() is False
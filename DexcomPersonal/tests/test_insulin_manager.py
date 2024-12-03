import pytest
from unittest.mock import Mock
from datetime import datetime, timedelta
from DexcomPersonal.insulin_manager import InsulinManager

class TestInsulinManager:
    @pytest.fixture
    def mock_insulin_pump(self):
        pump = Mock()
        pump.config.max_bolus = 10.0
        return pump

    @pytest.fixture
    def mock_data_manager(self):
        return Mock()

    @pytest.fixture
    def mock_cloud_sync(self):
        return Mock()

    @pytest.fixture
    def insulin_manager(self, mock_insulin_pump, mock_data_manager, mock_cloud_sync):
        return InsulinManager(mock_insulin_pump, mock_data_manager, mock_cloud_sync)

    def test_deliver_bolus_success(self, insulin_manager, mock_insulin_pump, mock_data_manager):
        units = 5.0
        insulin_manager.deliver_bolus(units)
        
        mock_insulin_pump.calculate_meal_bolus.assert_called_once_with(units)
        mock_data_manager.add_insulin_record.assert_called_once()

    def test_deliver_bolus_exceeds_max(self, insulin_manager):
        with pytest.raises(ValueError):
            insulin_manager.deliver_bolus(15.0)

    def test_deliver_bolus_too_frequent(self, insulin_manager):
        insulin_manager.deliver_bolus(5.0)
        with pytest.raises(ValueError):
            insulin_manager.deliver_bolus(5.0)  # Deuxième bolus trop rapproché

    def test_safety_constraints(self, insulin_manager):
        assert insulin_manager._check_safety_constraints(5.0) is True
        assert insulin_manager._check_safety_constraints(15.0) is False
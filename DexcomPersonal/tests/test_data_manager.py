import pytest
import sqlite3
from datetime import datetime, timedelta
from DexcomPersonal.data_manager import DataManager

class TestDataManager:
    @pytest.fixture
    def data_manager(self, tmp_path):
        db_path = tmp_path / "test.db"
        return DataManager(str(db_path))

    def test_add_glucose_reading(self, data_manager):
        timestamp = datetime.now()
        glucose_level = 120.0
        
        data_manager.add_glucose_reading(timestamp, glucose_level)
        
        df = data_manager.get_glucose_history(hours=1)
        assert len(df) == 1
        assert df.iloc[0]['glucose_level'] == glucose_level

    def test_add_insulin_record(self, data_manager):
        record = {
            'timestamp': datetime.now(),
            'units': 5.0,
            'type': 'bolus'
        }
        
        data_manager.add_insulin_record(record)
        
        df = data_manager.get_insulin_history(hours=1)
        assert len(df) == 1
        assert df.iloc[0]['units'] == 5.0

    def test_get_glucose_history(self, data_manager):
        now = datetime.now()
        
        # Ajouter données sur 48h
        for i in range(48):
            timestamp = now - timedelta(hours=i)
            data_manager.add_glucose_reading(timestamp, 120.0)
        
        # Tester récupération 24h
        df = data_manager.get_glucose_history(hours=24)
        assert len(df) == 24
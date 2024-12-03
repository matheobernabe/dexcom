import pytest
from unittest.mock import Mock
import pandas as pd
from datetime import datetime, timedelta
from DexcomPersonal.graph_manager import GraphManager

class TestGraphManager:
    @pytest.fixture
    def mock_data_manager(self):
        manager = Mock()
        # Créer des données de test
        dates = pd.date_range(start=datetime.now()-timedelta(days=1), 
                            end=datetime.now(), 
                            freq='5min')
        glucose_data = pd.DataFrame({
            'timestamp': dates,
            'glucose_level': [120] * len(dates)
        })
        manager.get_glucose_history.return_value = glucose_data
        return manager

    @pytest.fixture
    def graph_manager(self, mock_data_manager):
        return GraphManager(mock_data_manager)

    def test_generate_daily_graph(self, graph_manager):
        fig, stats = graph_manager.generate_daily_graph()
        assert fig is not None
        assert len(stats) == 4
        assert stats[0] == 100  # time in range
        assert stats[1] == 120  # average glucose

    def test_calculate_statistics(self, graph_manager):
        df = pd.DataFrame({
            'glucose_level': [70, 100, 150, 200]
        })
        stats = graph_manager._calculate_statistics(df)
        assert stats[0] == 75  # 3/4 in range
        assert stats[1] == 130  # average
        assert stats[2] == 200  # max
        assert stats[3] == 70   # min
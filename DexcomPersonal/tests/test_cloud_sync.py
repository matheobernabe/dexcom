import pytest
from unittest.mock import Mock, patch
from datetime import datetime
from DexcomPersonal.cloud_sync import CloudSync

class TestCloudSync:
    @pytest.fixture
    def cloud_sync(self):
        return CloudSync("http://api.example.com", "test_user")

    def test_sync_glucose_data_success(self, cloud_sync):
        glucose_data = {
            "timestamp": datetime.now(),
            "glucose_level": 120
        }
        
        with patch('requests.post') as mock_post:
            mock_post.return_value.status_code = 200
            assert cloud_sync.sync_glucose_data(glucose_data) is True

    def test_sync_glucose_data_failure(self, cloud_sync):
        glucose_data = {
            "timestamp": datetime.now(),
            "glucose_level": 120
        }
        
        with patch('requests.post') as mock_post:
            mock_post.return_value.status_code = 500
            assert cloud_sync.sync_glucose_data(glucose_data) is False
            assert len(cloud_sync.sync_queue) == 1

    def test_process_sync_queue(self, cloud_sync):
        glucose_data = {
            "timestamp": datetime.now(),
            "glucose_level": 120
        }
        cloud_sync.sync_queue.append(("glucose", glucose_data))
        
        with patch('requests.post') as mock_post:
            mock_post.return_value.status_code = 200
            cloud_sync.process_sync_queue()
            assert len(cloud_sync.sync_queue) == 0
import unittest
import requests
import sys
import os
from unittest.mock import patch

# Ajoutez le chemin racine du projet
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

BASE_URL = "http://localhost:6000"

class TestGlucoseSensor(unittest.TestCase):

    def test_sensor_status(self):
        """Test l'endpoint de statut du capteur."""
        response = requests.get(f"{BASE_URL}/sensor-status")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("sensor_id", data)
        self.assertIn("status", data)
        self.assertEqual(data["status"], "OK")

    def test_glucose_endpoint(self):
        """Test l'endpoint de simulation de glucose."""
        response = requests.get(f"{BASE_URL}/glucose")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("sensor_id", data)
        self.assertIn("glucose_level", data)
        self.assertTrue(70 <= data["glucose_level"] <= 150)

    @patch('requests.post')
    def test_send_to_dexcom_personal(self, mock_post):
        """Mock le comportement d'envoi à Dexcom Personal."""
        from app import send_to_dexcom_personal
        mock_post.return_value.status_code = 200

        glucose_level = 110
        send_to_dexcom_personal(glucose_level)

        # Vérifie qu'un seul appel a été fait
        mock_post.assert_called_once_with(
            'http://localhost:6002/api/glucose',
            json={
                "sensor_id": "1234",
                "glucose_level": glucose_level,
                "status": "OK"
            }
        )

if __name__ == '__main__':
    unittest.main()

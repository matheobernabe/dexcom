import unittest
from unittest.mock import patch
from GlucoseSensor.app import app, generate_glucose, send_to_dexcom_personal

class TestGlucoseSensor(unittest.TestCase):

    def test_generate_glucose(self):
        """Test de génération de données de glucose."""
        glucose_level = generate_glucose()
        self.assertTrue(60 <= glucose_level <= 190)

    @patch("requests.post")
    def test_send_to_dexcom_personal(self, mock_post):
        """Test d'envoi des données à Dexcom Personal."""
        mock_post.return_value.status_code = 200

        glucose_level = 120
        send_to_dexcom_personal(glucose_level)
        mock_post.assert_called_once_with(
            "http://localhost:6002/api/glucose",
            json={
                "sensor_id": "1234",
                "glucose_level": glucose_level,
                "status": "OK"
            }
        )

    def test_sensor_status(self):
        """Test de l'état du capteur."""
        with app.test_client() as client:
            response = client.get('/sensor-status')
            self.assertEqual(response.status_code, 200)
            self.assertIn("status", response.json)
            self.assertEqual(response.json["status"], "OK")

    def test_get_glucose(self):
        """Test de l'endpoint glucose."""
        with app.test_client() as client:
            response = client.get('/glucose')
            self.assertEqual(response.status_code, 200)
            self.assertIn("glucose_level", response.json)
            self.assertTrue(60 <= response.json["glucose_level"] <= 190)


if __name__ == "__main__":
    unittest.main()

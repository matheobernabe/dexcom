import unittest
from unittest.mock import patch
from DexcomPersonal.app import app

class TestDexcomPersonal(unittest.TestCase):

    @patch("requests.post")
    def test_receive_glucose_data_success(self, mock_post):
        """Test de réception de données avec succès."""
        mock_post.return_value.status_code = 200

        with app.test_client() as client:
            payload = {
                "sensor_id": "1234",
                "glucose_level": 110,
                "status": "OK"
            }
            response = client.post('/api/glucose', json=payload)

            self.assertEqual(response.status_code, 200)
            self.assertIn("status", response.json)
            self.assertEqual(response.json["status"], "success")

    def test_receive_glucose_data_invalid(self):
        """Test de réception de données invalides."""
        with app.test_client() as client:
            response = client.post('/api/glucose', json={})
            self.assertEqual(response.status_code, 400)
            self.assertIn("error", response.json)

    def test_health_check(self):
        """Test de vérification de l'état de l'application."""
        with app.test_client() as client:
            response = client.get('/status')
            self.assertEqual(response.status_code, 200)
            self.assertIn("status", response.json)
            self.assertEqual(response.json["status"], "Dexcom Personal is running")


if __name__ == "__main__":
    unittest.main()

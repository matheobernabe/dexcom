import unittest
from unittest.mock import patch
from DexcomCloud.app import app

class TestDexcomCloud(unittest.TestCase):

    def test_data_validation_success(self):
        """Test de validation des données avec succès."""
        with app.test_client() as client:
            payload = {
                "sensor_id": "1234",
                "glucose_level": 110,
                "status": "OK"
            }
            response = client.post('/api/data-validation', json=payload)
            self.assertEqual(response.status_code, 200)
            self.assertIn("status", response.json)
            self.assertEqual(response.json["status"], "success")

    def test_data_validation_invalid(self):
        """Test de validation des données invalides."""
        with app.test_client() as client:
            payload = {
                "sensor_id": "1234",
                "glucose_level": 20,  # Niveau de glucose invalide
                "status": "OK"
            }
            response = client.post('/api/data-validation', json=payload)
            self.assertEqual(response.status_code, 400)
            self.assertIn("error", response.json)

    @patch("DataProcessor.kafka_producer.KafkaProducer.send_alert")
    def test_alert_manager_hypoglycemia(self, mock_send_alert):
        """Test d'alerte pour hypoglycémie."""
        with app.test_client() as client:
            payload = {
                "sensor_id": "1234",
                "glucose_level": 60  # Hypoglycémie
            }
            response = client.post('/api/alert-manager', json=payload)
            self.assertEqual(response.status_code, 200)
            self.assertIn("alert", response.json)

            # Vérifie que l'alerte est envoyée à Kafka
            mock_send_alert.assert_called_once()

    def test_health_check(self):
        """Test de vérification de l'état de l'application."""
        with app.test_client() as client:
            response = client.get('/status')
            self.assertEqual(response.status_code, 200)
            self.assertIn("status", response.json)
            self.assertEqual(response.json["status"], "Dexcom Cloud is running")


if __name__ == "__main__":
    unittest.main()

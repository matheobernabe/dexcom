import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, patch
import random

from cgm.advanced_cgm import AdvancedCGM
from cgm.glucose_analyzer import GlucoseAnalyzer
from cgm.sensor_monitor import SensorMonitor
from cgm.kafka_producer import GlucoseKafkaProducer

class TestGlucoseAnalyzer:
    @pytest.fixture
    def kafka_mock(self):
        mock = Mock(spec=GlucoseKafkaProducer)
        mock.ALERT_TOPIC = 'glucose_alerts'
        return mock

    @pytest.fixture
    def analyzer(self, kafka_mock):
        return GlucoseAnalyzer(kafka_mock)

    def test_analyze_glucose_hypo(self, analyzer, kafka_mock):
        timestamp = datetime.now().isoformat()
        analyzer.analyze_glucose(65, timestamp)

        kafka_mock.send_message.assert_called_once_with(
            kafka_mock.ALERT_TOPIC,
            {
                'timestamp': timestamp,
                'type': 'HYPOGLYCEMIA',
                'level': 'URGENT',
                'glucose_level': 65,
                'threshold': 70,
                'message': 'Hypoglycémie détectée'
            }
        )

    def test_analyze_glucose_hyper(self, analyzer, kafka_mock):
        timestamp = datetime.now().isoformat()
        analyzer.analyze_glucose(190, timestamp)

        kafka_mock.send_message.assert_called_once_with(
            kafka_mock.ALERT_TOPIC,
            {
                'timestamp': timestamp,
                'type': 'HYPERGLYCEMIA',
                'level': 'WARNING',
                'glucose_level': 190,
                'threshold': 180,
                'message': 'Hyperglycémie détectée'
            }
        )

    def test_analyze_glucose_normal(self, analyzer, kafka_mock):
        timestamp = datetime.now().isoformat()
        analyzer.analyze_glucose(100, timestamp)
        kafka_mock.send_message.assert_not_called()

class TestSensorMonitor:
    @pytest.fixture
    def kafka_mock(self):
        mock = Mock(spec=GlucoseKafkaProducer)
        mock.STATUS_TOPIC = 'sensor_status'  # Ajouter l'attribut STATUS_TOPIC
        return mock

    @pytest.fixture
    def monitor(self, kafka_mock):
        with patch('cgm.sensor_monitor.datetime') as mock_datetime:
            mock_datetime.now.return_value = datetime(2024, 1, 1)
            return SensorMonitor(kafka_mock)

    def test_sensor_lifetime_valid(self, monitor, kafka_mock):
        with patch('cgm.sensor_monitor.datetime') as mock_datetime:
            mock_datetime.now.return_value = datetime(2024, 1, 5)
            assert monitor.check_sensor_lifetime() is True

    def test_sensor_lifetime_expired(self, monitor, kafka_mock):
        with patch('cgm.sensor_monitor.datetime') as mock_datetime:
            mock_datetime.now.return_value = datetime(2024, 1, 12)
            assert monitor.check_sensor_lifetime() is False
            kafka_mock.send_message.assert_called_once_with(
                kafka_mock.STATUS_TOPIC,  # Utiliser l'attribut simulé
                {'timestamp': '2024-01-12T00:00:00',
                 'status': 'EXPIRED',
                 'message': 'Capteur expiré - Remplacement nécessaire'}
            )

class TestAdvancedCGM:
    @pytest.fixture
    def patient_mock(self):
        patient = Mock()
        patient.glucose_level = 120
        return patient

    @pytest.fixture
    def cgm(self):
        return AdvancedCGM(target_glucose=120)

    def test_measure_glucose_precision(self, cgm, patient_mock):
        base_glucose = patient_mock.glucose_level
        measure = cgm.measure_glucose(patient_mock)
        assert measure is not None
        assert base_glucose * 0.9 <= measure <= base_glucose * 1.1

    def test_measure_glucose_expired_sensor(self, cgm, patient_mock):
        cgm.sensor_monitor.expiration_time = datetime.now() - timedelta(days=1)
        measure = cgm.measure_glucose(patient_mock)
        assert measure is None

    @patch('time.sleep')  # Pour éviter d'attendre réellement
    def test_continuous_monitoring(self, mock_sleep, cgm, patient_mock):
        measurements = []

        def mock_measure(*args):
            if len(measurements) >= 3:  # Arrêter après 3 mesures
                cgm.sensor_monitor.expiration_time = datetime.now() - timedelta(days=1)  # Simuler capteur expiré
            glucose_value = 120 * random.uniform(0.9, 1.1)
            measurements.append(glucose_value)
            return glucose_value

        with patch.object(cgm.sensor_monitor, 'check_sensor_lifetime', side_effect=[True, True, True, False]):
            with patch.object(cgm, 'measure_glucose', side_effect=mock_measure):
                cgm.start_continuous_monitoring(patient_mock)

        # Assertions
        assert len(measurements) == 3
        for measure in measurements:
            assert 108 <= measure <= 132  # ±10% de 120

import random
import time
from datetime import datetime

from .kafka_producer import GlucoseKafkaProducer
from .sensor_monitor import SensorMonitor
from .glucose_analyzer import GlucoseAnalyzer

class AdvancedCGM:
    def __init__(self, target_glucose=120):
        self.measurement_interval = 5  # minutes
        self.target_glucose = target_glucose
        self.last_measurement = None
        
        # Initialisation des composants
        self.kafka_producer = GlucoseKafkaProducer()
        self.sensor_monitor = SensorMonitor(self.kafka_producer)
        self.glucose_analyzer = GlucoseAnalyzer(self.kafka_producer)

    def measure_glucose(self, patient):
        """Effectue une mesure de glucose avec précision ±10%"""
        if not self.sensor_monitor.check_sensor_lifetime():
            return None
            
        # Mesure de base du patient
        base_glucose = patient.glucose_level
        
        # Ajout de l'imprécision ±10%
        accuracy_variation = random.uniform(-0.10, 0.10)
        measured_glucose = base_glucose * (1 + accuracy_variation)
        measured_glucose = round(measured_glucose, 1)
        
        # Timestamp de la mesure
        measurement_time = datetime.now().isoformat()
        
        # Création du message de mesure
        measurement_data = {
            'timestamp': measurement_time,
            'glucose_level': measured_glucose,
            'unit': 'mg/dL'
        }
        
        # Envoi de la mesure
        self.kafka_producer.send_message(
            self.kafka_producer.GLUCOSE_TOPIC, 
            measurement_data
        )
        
        # Analyse du glucose
        self.glucose_analyzer.analyze_glucose(measured_glucose, measurement_time)
        
        self.last_measurement = measured_glucose
        return measured_glucose

    def start_continuous_monitoring(self, patient):
        """Démarre le monitoring continu"""
        while self.sensor_monitor.check_sensor_lifetime():
            glucose = self.measure_glucose(patient)
            if glucose is not None:
                time.sleep(self.measurement_interval * 60)

    def set_thresholds(self, hypo=None, hyper=None):
        """Configure les seuils d'alerte"""
        self.glucose_analyzer.set_thresholds(hypo, hyper)
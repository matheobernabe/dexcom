from kafka import KafkaConsumer
import json
from datetime import datetime

class GlucoseConsumer:
    def __init__(self, data_manager, alert_manager):
        self.consumer = KafkaConsumer(
            'glucose_measurements',
            'glucose_alerts',
            bootstrap_servers=['localhost:9092'],
            value_deserializer=lambda x: json.loads(x.decode('utf-8')),
            group_id='dexcom_personal_app',
            auto_offset_reset='latest'
        )
        self.data_manager = data_manager
        self.alert_manager = alert_manager

    def start_listening(self):
        """Démarre l'écoute des messages Kafka"""
        for message in self.consumer:
            if message.topic == 'glucose_measurements':
                self._handle_glucose_measurement(message.value)
            elif message.topic == 'glucose_alerts':
                self._handle_glucose_alert(message.value)

    def _handle_glucose_measurement(self, data):
        """Traite une nouvelle mesure de glucose"""
        self.data_manager.add_glucose_reading(
            timestamp=datetime.fromisoformat(data['timestamp']),
            glucose_level=data['glucose_level']
        )

    def _handle_glucose_alert(self, alert):
        """Traite une alerte de glucose"""
        self.alert_manager.process_alert(alert)
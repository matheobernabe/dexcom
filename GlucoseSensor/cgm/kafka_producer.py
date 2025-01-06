from kafka import KafkaProducer
import json

class GlucoseKafkaProducer:
    def __init__(self):
        self.producer = KafkaProducer(
            bootstrap_servers=['localhost:9092'],
            value_serializer=lambda x: json.dumps(x).encode('utf-8')
        )
        
        # Topics Kafka
        self.GLUCOSE_TOPIC = 'glucose_measurements'
        self.ALERT_TOPIC = 'glucose_alerts'
        self.STATUS_TOPIC = 'sensor_status'

    def send_message(self, topic, message):
        """Envoie un message à un topic Kafka"""
        try:
            future = self.producer.send(topic, message)
            future.get(timeout=10)
            return True
        except Exception as e:
            print(f"Erreur d'envoi Kafka: {str(e)}")
            return False
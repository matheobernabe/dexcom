from decimal import Decimal
from datetime import datetime
from confluent_kafka import Producer
import json

class KafkaProducer:
    def __init__(self, bootstrap_servers='localhost:9092'):
        """Initialise le producteur Kafka."""
        self.producer = Producer({'bootstrap.servers': bootstrap_servers})
        self.VALIDATED_TOPIC = 'validated_data'
        self.ALERTS_TOPIC = 'alerts'

    def delivery_report(self, err, msg):
        """Callback appelé après la livraison d'un message."""
        if err is not None:
            print(f"Message delivery failed: {err}")
        else:
            print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

    def serialize_data(self, data):
        """Convertit les objets non JSON-sérialisables en types compatibles."""
        return json.dumps(data, default=self.json_serializer)

    def json_serializer(self, obj):
        """Sérialiseur personnalisé pour les objets non standard."""
        if isinstance(obj, Decimal):
            return float(obj)  # Convertir Decimal en float
        if isinstance(obj, datetime):
            return obj.isoformat()  # Convertir datetime en format ISO 8601
        raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")

    def send_validated_data(self, data):
        """Envoie les données validées au topic Kafka."""
        try:
            self.producer.produce(
                self.VALIDATED_TOPIC,
                key=str(data.get('sensor_id', 'unknown')),
                value=self.serialize_data(data),
                callback=self.delivery_report
            )
            self.producer.flush()
        except Exception as e:
            print(f"Error sending validated data to Kafka: {e}")

    def send_alert(self, alert):
        """Envoie une alerte au topic Kafka."""
        try:
            self.producer.produce(
                self.ALERTS_TOPIC,
                key=str(alert.get('type', 'unknown')),
                value=self.serialize_data(alert),
                callback=self.delivery_report
            )
            self.producer.flush()
        except Exception as e:
            print(f"Error sending alert to Kafka: {e}")

import KafkaProducer
import json
from database import save_alert

class AlertManager:
    def __init__(self):
        self.producer = KafkaProducer(
            bootstrap_servers=["localhost:9092"],
            value_serializer=lambda x: json.dumps(x).encode("utf-8"),
        )

    def analyze_and_alert(self, data):
        glucose_level = data.get("glucose_level")
        if glucose_level:
            if glucose_level < 70:
                alert = self.create_alert("HYPOGLYCEMIA", "Low glucose level detected!", glucose_level)
                self.send_alert(alert)
            elif glucose_level > 180:
                alert = self.create_alert("HYPERGLYCEMIA", "High glucose level detected!", glucose_level)
                self.send_alert(alert)

    def create_alert(self, alert_type, message, glucose_level):
        """Crée une alerte au format JSON."""
        return {
            "type": alert_type,
            "message": message,
            "glucose_level": glucose_level,
        }

    def send_alert(self, alert):
        """Envoie une alerte au topic Kafka et stocke dans la BDD."""
        self.producer.send("glucose_alerts", value=alert)
        save_alert(alert)

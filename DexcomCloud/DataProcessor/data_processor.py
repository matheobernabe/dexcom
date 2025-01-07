import KafkaConsumer
import json
from database import save_validated_data

class DataProcessor:
    def __init__(self):
        self.consumer = KafkaConsumer(
            "glucose_measurements",
            bootstrap_servers=["localhost:9092"],
            auto_offset_reset="earliest",
            value_deserializer=lambda x: json.loads(x.decode("utf-8")),
        )

    def process_data(self):
        for message in self.consumer:
            data = message.value
            if self.validate_data(data):
                save_validated_data(data)

    @staticmethod
    def validate_data(data):
        """Valide les données en fonction de règles prédéfinies."""
        if "glucose_level" in data and 40 <= data["glucose_level"] <= 400:
            return True
        return False

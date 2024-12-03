from flask import Flask, jsonify
from confluent_kafka import Producer
import logging

class Publisher:
    def __init__(self, kafka_server="kafka:9092", topic="glucose_data", host="0.0.0.0", port=6000):
        # Initialisation Flask
        self.app = Flask(__name__)
        self.host = host
        self.port = port

        # Initialisation Kafka Producer
        self.kafka_server = kafka_server
        self.topic = topic
        self.producer = Producer({"bootstrap.servers": self.kafka_server})

        # Routes Flask
        self._setup_routes()

    def _setup_routes(self):
        @self.app.route("/status", methods=["GET"])
        def status():
            return jsonify({"status": "running"})

    def send_event_to_kafka(self, data):
        """Envoie un message au topic Kafka."""
        try:
            self.producer.produce(self.topic, value=str(data))
            self.producer.flush()
            logging.info(f"Message envoyé à Kafka : {data}")
        except Exception as e:
            logging.error(f"Erreur lors de l'envoi à Kafka : {e}")

    def run(self):
        """Démarre le serveur Flask."""
        logging.info(f"Publisher démarré sur {self.host}:{self.port}")
        self.app.run(host=self.host, port=self.port)

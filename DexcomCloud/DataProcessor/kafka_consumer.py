from confluent_kafka import Consumer
import json

class KafkaConsumerService:
    def __init__(self, bootstrap_servers='localhost:9092', group_id='dexcom_cloud'):
        """Initialise le consommateur Kafka."""
        self.consumer = Consumer({
            'bootstrap.servers': bootstrap_servers,
            'group.id': group_id,
            'auto.offset.reset': 'earliest'
        })

    def subscribe_to_topics(self, topics):
        """Souscrit à une liste de topics."""
        self.consumer.subscribe(topics)

    def consume_messages(self):
        """Consomme les messages des topics souscrits."""
        try:
            while True:
                msg = self.consumer.poll(1.0)  # Timeout de 1 seconde
                if msg is None:
                    continue
                if msg.error():
                    print(f"Consumer error: {msg.error()}")
                    continue

                # Traitez ici le message reçu
                message_data = json.loads(msg.value().decode('utf-8'))
                print(f"Received message: {message_data}")
        except KeyboardInterrupt:
            print("Consumer interrupted")
        finally:
            self.consumer.close()

from confluent_kafka import Consumer
import logging

# Configuration du journal
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

# Configuration du Consumer
consumer_config = {
    "bootstrap.servers": "localhost:9092",
    "group.id": "clarity_group",  # Chaque service peut avoir son propre group_id
    "auto.offset.reset": "earliest"
}

def consume_glucose_data():
    consumer = Consumer(consumer_config)
    consumer.subscribe(["glucose_data"])  # S'abonner au topic

    try:
        while True:
            msg = consumer.poll(1.0)  # Attendre un message pendant 1 seconde
            if msg is None:
                continue
            if msg.error():
                logging.error(f"Erreur Kafka : {msg.error()}")
                continue

            # Traiter le message reçu
            data = msg.value().decode("utf-8")
            logging.info(f"Message reçu : {data}")
    except KeyboardInterrupt:
        logging.info("Arrêt du Consumer.")
    finally:
        consumer.close()

if __name__ == "__main__":
    consume_glucose_data()

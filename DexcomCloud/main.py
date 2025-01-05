from DataProcessor.publisher import Publisher
import requests
import threading
import time
import schedule
import logging

# Configuration du journal
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

# URL de l'API du capteur de glucose
SENSOR_API_URL = "http://localhost:6000/glucose"

# Intervalle pour récupérer les données (en minutes)
FETCH_INTERVAL = 5

# Fonction pour récupérer les données de glucose et les envoyer à Kafka
def fetch_and_publish(publisher):
    try:
        response = requests.get(SENSOR_API_URL, timeout=10)
        if response.status_code == 200:
            data = response.json()
            logging.info(f"Nouvelle donnée reçue : {data}")
            # Envoyer les données à Kafka
            publisher.send_event_to_kafka(data)
        else:
            logging.error(f"Erreur lors de la récupération des données : {response.status_code}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Erreur de connexion au capteur : {e}")

# Planification des tâches périodiques
def start_scheduler(publisher):
    schedule.every(FETCH_INTERVAL).minutes.do(fetch_and_publish, publisher=publisher)
    while True:
        schedule.run_pending()
        time.sleep(1)

# Point d'entrée principal
if __name__ == "__main__":
    # Initialiser le publisher avec Kafka
    publisher = Publisher(kafka_server="kafka:9092", topic="glucose_data")

    # Lancer le scheduler dans un thread séparé
    scheduler_thread = threading.Thread(target=start_scheduler, args=(publisher,))
    scheduler_thread.daemon = True
    scheduler_thread.start()

    # Démarrer le serveur Flask
    publisher.run()

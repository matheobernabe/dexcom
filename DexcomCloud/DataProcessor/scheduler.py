import schedule
import time
import requests
import logging

class Scheduler:
    def __init__(self, publisher, fetch_url, interval=5):
        self.publisher = publisher
        self.fetch_url = fetch_url
        self.interval = interval

    def fetch_and_emit(self):
        try:
            response = requests.get(self.fetch_url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                logging.info(f"Nouvelle donnée reçue : {data}")
                self.publisher.emit_event("glucose_update", data)
            else:
                logging.error(f"Erreur lors de la récupération des données : {response.status_code}")
        except requests.exceptions.RequestException as e:
            logging.error(f"Erreur de connexion au capteur : {e}")

    def start(self):
        """Planifie la tâche et l'exécute périodiquement."""
        schedule.every(self.interval).minutes.do(self.fetch_and_emit)
        while True:
            schedule.run_pending()
            time.sleep(1)

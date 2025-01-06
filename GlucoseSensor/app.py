from flask import Flask, jsonify, request
import random
import time
import threading
import requests

app = Flask(__name__)

# Configuration
DEXCOM_PERSONAL_URL = "http://localhost:6002/api/glucose"  # Endpoint de Dexcom Personal
SEND_INTERVAL = 60  # Intervalle en secondes entre chaque envoi de données

# Simulation de données de glycémie
def generate_glucose():
    """Génère un taux de glucose simulé entre 70 et 150 mg/dL."""
    return round(random.uniform(60, 190), 1)

def send_to_dexcom_personal(glucose_level):
    """Envoie les données au serveur Dexcom Personal."""
    data = {
        "sensor_id": "1234",
        "glucose_level": glucose_level,
        "status": "OK"
    }
    try:
        response = requests.post(DEXCOM_PERSONAL_URL, json=data)
        if response.status_code == 200:
            print(f"Data sent successfully: {data}")
        else:
            print(f"Failed to send data: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Error while sending data: {e}")

# Tâche en arrière-plan pour envoyer les données périodiquement
def background_task():
    """Tâche d'émulation et d'envoi des données."""
    while True:
        glucose_level = generate_glucose()
        send_to_dexcom_personal(glucose_level)
        time.sleep(SEND_INTERVAL)

# Démarrage de la tâche en arrière-plan
thread = threading.Thread(target=background_task, daemon=True)
thread.start()

# Endpoint API pour vérifier le statut du capteur
@app.route('/sensor-status', methods=['GET'])
def sensor_status():
    """Renvoie l'état du capteur (fictif)."""
    return jsonify({"sensor_id": "1234", "status": "OK"})

# Endpoint pour afficher une simulation de mesure
@app.route('/glucose', methods=['GET'])
def get_glucose():
    """Simule et renvoie un taux de glucose."""
    glucose_level = generate_glucose()
    return jsonify({"sensor_id": "1234", "glucose_level": glucose_level, "status": "OK"})

if __name__ == '__main__':
    # Démarrage de la tâche en arrière-plan uniquement en mode exécution
    thread = threading.Thread(target=background_task, daemon=True)
    thread.start()
    app.run(host='0.0.0.0', port=6000)

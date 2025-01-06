from flask import Flask, request, jsonify
import time
from DataProcessor.kafka_producer import KafkaProducer

app = Flask(__name__)

# Initialisation du producteur Kafka
kafka_producer = KafkaProducer()

# Simuler une base de données pour stocker les données validées et les alertes
validated_data_store = []
alert_store = []

@app.route('/api/data-validation', methods=['POST'])
def data_validation():
    """Valide les données reçues de Dexcom Personal."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data received"}), 400

    # Exemple de validation simple
    if "glucose_level" in data and 40 <= data["glucose_level"] <= 400:
        validated_data_store.append(data)
        
        # Envoi des données validées à Kafka
        kafka_producer.send_validated_data(data)

        return jsonify({"status": "success", "validated_data": data}), 200
    else:
        return jsonify({"error": "Invalid glucose level"}), 400

@app.route('/api/alert-manager', methods=['POST'])
def alert_manager():
    """Gère les alertes basées sur les données reçues."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data received"}), 400

    # Gestion des seuils
    glucose_level = data.get("glucose_level")
    if glucose_level:
        if glucose_level < 70:
            alert = {
                "type": "HYPOGLYCEMIA",
                "message": "Low glucose level detected!",
                "glucose_level": glucose_level,
                "timestamp": time.time(),
            }
            alert_store.append(alert)

            # Envoi de l'alerte à Kafka
            kafka_producer.send_alert(alert)

            return jsonify({"status": "alert", "alert": alert}), 200
        elif glucose_level > 180:
            alert = {
                "type": "HYPERGLYCEMIA",
                "message": "High glucose level detected!",
                "glucose_level": glucose_level,
                "timestamp": time.time(),
            }
            alert_store.append(alert)

            # Envoi de l'alerte à Kafka
            kafka_producer.send_alert(alert)

            return jsonify({"status": "alert", "alert": alert}), 200
    return jsonify({"status": "no_alert", "glucose_level": glucose_level}), 200

@app.route('/validated-data', methods=['GET'])
def get_validated_data():
    """Renvoie toutes les données validées stockées."""
    return jsonify({"validated_data": validated_data_store}), 200

@app.route('/alerts', methods=['GET'])
def get_alerts():
    """Renvoie toutes les alertes stockées."""
    return jsonify({"alerts": alert_store}), 200

@app.route('/status', methods=['GET'])
def health_check():
    """Vérifie si le service est en ligne."""
    return jsonify({"status": "Dexcom Cloud is running"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6003)

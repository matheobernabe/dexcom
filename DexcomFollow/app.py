from flask import Flask, jsonify, request
from confluent_kafka import Consumer, KafkaException
import threading
import json

app = Flask(__name__)

# Configuration
KAFKA_BROKER = "localhost:9092"  # Adresse du broker Kafka
GLUCOSE_TOPIC = "glucose_measurements"  # Topic Kafka pour les données de glucose
ALERT_TOPIC = "glucose_alerts"  # Topic Kafka pour les alertes
PATIENT_ID = "patient_1234"  # ID du patient que Dexcom Follow suit

# Stockage en mémoire pour les données
glucose_data = []
alerts = []

# Configuration du consommateur Kafka
consumer_config = {
    'bootstrap.servers': KAFKA_BROKER,
    'group.id': 'dexcom_follow_group',
    'auto.offset.reset': 'latest',
}

# Fonction pour écouter Kafka et filtrer les messages par patient_id
def consume_kafka_messages():
    consumer = Consumer(consumer_config)
    consumer.subscribe([GLUCOSE_TOPIC, ALERT_TOPIC])

    try:
        while True:
            msg = consumer.poll(1.0)  # Attendre les messages pendant 1 seconde
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaException._PARTITION_EOF:
                    continue
                else:
                    print(f"Erreur Kafka: {msg.error()}")
                    continue

            # Décodage du message
            try:
                message_value = json.loads(msg.value().decode('utf-8'))
                topic = msg.topic()

                # Filtrer par patient_id
                if topic == GLUCOSE_TOPIC and message_value.get("patient_id") == PATIENT_ID:
                    glucose_data.append(message_value)
                    print(f"Glucose Data Received: {message_value}")
                elif topic == ALERT_TOPIC and message_value.get("patient_id") == PATIENT_ID:
                    alerts.append(message_value)
                    print(f"Alert Received: {message_value}")
            except Exception as e:
                print(f"Erreur lors du traitement du message: {e}")

    except Exception as e:
        print(f"Erreur dans le consommateur Kafka: {e}")
    finally:
        consumer.close()

# Lancer la consommation Kafka dans un thread séparé
threading.Thread(target=consume_kafka_messages, daemon=True).start()

# Endpoint pour afficher les données de glucose
@app.route('/patient/<patient_id>/glucose', methods=['GET'])
def get_glucose_data(patient_id):
    if patient_id != PATIENT_ID:
        return jsonify({"error": "Patient not found"}), 404

    return jsonify({"patient_id": patient_id, "glucose_data": glucose_data}), 200

# Endpoint pour afficher les alertes du patient
@app.route('/patient/<patient_id>/alerts', methods=['GET'])
def get_alerts(patient_id):
    if patient_id != PATIENT_ID:
        return jsonify({"error": "Patient not found"}), 404

    return jsonify({"patient_id": patient_id, "alerts": alerts}), 200

# Endpoint pour vérifier que Dexcom Follow fonctionne
@app.route('/status', methods=['GET'])
def health_check():
    return jsonify({"status": "Dexcom Follow is running"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6003)

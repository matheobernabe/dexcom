from flask import Flask, request, jsonify
import time
from DataProcessor.database import get_db_connection, create_tables
from DataProcessor.kafka_producer import KafkaProducer

app = Flask(__name__)

# Initialisation
kafka_producer = KafkaProducer()
create_tables()

@app.route('/api/data-validation', methods=['POST'])
def data_validation():
    """Valide les données reçues de Dexcom Personal et enregistre dans la BDD."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data received"}), 400

    if "glucose_level" in data and 40 <= data["glucose_level"] <= 400:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO validated_data (sensor_id, glucose_level, status)
            VALUES (%s, %s, %s)
            RETURNING *;
        """, (data.get("sensor_id"), data.get("glucose_level"), data.get("status")))
        validated_data = cursor.fetchone()
        connection.commit()
        cursor.close()
        connection.close()

        # Envoi des données validées à Kafka
        kafka_producer.send_validated_data(validated_data)

        return jsonify({"status": "success", "validated_data": validated_data}), 200
    else:
        return jsonify({"error": "Invalid glucose level"}), 400

@app.route('/api/alert-manager', methods=['POST'])
def alert_manager():
    """Gère les alertes basées sur les données reçues et les enregistre dans la BDD."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data received"}), 400

    glucose_level = data.get("glucose_level")
    if glucose_level:
        alert = None
        if glucose_level < 70:
            alert = {
                "type": "HYPOGLYCEMIA",
                "message": "Low glucose level detected!",
                "glucose_level": glucose_level,
            }
        elif glucose_level > 180:
            alert = {
                "type": "HYPERGLYCEMIA",
                "message": "High glucose level detected!",
                "glucose_level": glucose_level,
            }

        if alert:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO alerts (type, message, glucose_level)
                VALUES (%s, %s, %s)
                RETURNING *;
            """, (alert["type"], alert["message"], alert["glucose_level"]))
            saved_alert = cursor.fetchone()
            connection.commit()
            cursor.close()
            connection.close()

            # Envoi de l'alerte à Kafka
            kafka_producer.send_alert(saved_alert)

            return jsonify({"status": "alert", "alert": saved_alert}), 200

    return jsonify({"status": "no_alert"}), 200

@app.route('/validated-data', methods=['GET'])
def get_validated_data():
    """Renvoie toutes les données validées stockées."""
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM validated_data;")
    validated_data = cursor.fetchall()
    cursor.close()
    connection.close()

    return jsonify({"validated_data": validated_data}), 200

@app.route('/alerts', methods=['GET'])
def get_alerts():
    """Renvoie toutes les alertes stockées."""
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM alerts;")
    alert_data = cursor.fetchall()
    cursor.close()
    connection.close()

    return jsonify({"alerts": alert_data}), 200

@app.route('/status', methods=['GET'])
def health_check():
    """Vérifie si le service est en ligne."""
    return jsonify({"status": "Dexcom Cloud is running"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6003)

from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Configuration
DEXCOM_CLOUD_DATA_VALIDATION_URL = "http://localhost:6003/api/data-validation"  # Endpoint pour la validation des données
DEXCOM_CLOUD_ALERT_MANAGER_URL = "http://localhost:6003/api/alert-manager"  # Endpoint pour la gestion des alertes

@app.route('/api/glucose', methods=['POST'])
def receive_glucose_data():
    """Reçoit les données de glucose et les envoie à Dexcom Cloud."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data received"}), 400

    # Envoi des données à DataValidation
    try:
        data_validation_response = requests.post(DEXCOM_CLOUD_DATA_VALIDATION_URL, json=data)
        if data_validation_response.status_code != 200:
            return jsonify({"error": "Failed to send data to DataValidation", 
                            "details": data_validation_response.text}), data_validation_response.status_code

        print(f"Data sent to DataValidation: {data}")
    except Exception as e:
        return jsonify({"error": f"Error while sending data to DataValidation: {str(e)}"}), 500

    # Envoi des données à AlertManager
    try:
        alert_manager_response = requests.post(DEXCOM_CLOUD_ALERT_MANAGER_URL, json=data)
        if alert_manager_response.status_code != 200:
            return jsonify({"error": "Failed to send data to AlertManager", 
                            "details": alert_manager_response.text}), alert_manager_response.status_code

        print(f"Data sent to AlertManager: {data}")
    except Exception as e:
        return jsonify({"error": f"Error while sending data to AlertManager: {str(e)}"}), 500

    return jsonify({"status": "success", "data": data}), 200

@app.route('/status', methods=['GET'])
def health_check():
    """Vérifie si le service est en ligne."""
    return jsonify({"status": "Dexcom Personal is running"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6002)

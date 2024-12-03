from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/glucose', methods=['GET'])
def get_glucose():
    # Simulation d'une mesure de glucose
    return jsonify({"sensorId": "1234", "glucoseLevel": 110, "status": "OK"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000)

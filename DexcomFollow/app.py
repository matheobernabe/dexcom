from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/follow', methods=['GET'])
def follow_data():
    # Simulation du suivi des données en temps réel
    return jsonify({"message": "Following glucose data in real time"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6004)

from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/process', methods=['POST'])
def process_data():
    # Simulation du traitement des données
    return jsonify({"message": "Data processed and stored successfully"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6003)

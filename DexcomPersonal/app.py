from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/display', methods=['GET'])
def display_data():
    # Simulation de l'affichage des données
    return jsonify({"message": "Displaying glucose data on personal device"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6002)

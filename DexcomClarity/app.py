from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/report', methods=['GET'])
def generate_report():
    # Simulation de la génération d'un rapport
    return jsonify({"message": "Report generated successfully"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6005)

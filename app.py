from flask import Flask, request, jsonify
from flask_cors import CORS
from shots import fetch_shots


app = Flask(__name__)
CORS(app)

@app.route('/shots', methods=["GET"])
def get_shots():
    params = {
        "playerId": request.args.get("playerId", default=None, type=int),
        "gameId": request.args.get("gameId", default=None, type=int),
        "strength": request.args.get("strength", default=None, type=str),
        "eventTypeId": request.args.get("eventTypeId", default=None, type=str),
        "secondaryType": request.args.get("secondaryType", default=None, type=str)
    }
    shots = fetch_shots(params)
    return jsonify(shots)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int("5000"), debug=True)
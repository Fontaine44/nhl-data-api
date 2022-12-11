from flask import Flask, request, jsonify
from flask_cors import CORS
from shots import fetch_shots, kde


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
    payload = {
        "shots": shots,
        "kde": kde(shots)
    }
    return jsonify(payload)
    

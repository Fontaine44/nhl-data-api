from flask import Flask, request, jsonify
from flask_cors import CORS
from shots import fetch_shots, kde
from db import fetch_logs


app = Flask(__name__)
CORS(app)


@app.route('/start', methods=["GET"])
def start_server():
    return jsonify({"success": True})


@app.route('/shots', methods=["GET"])
def get_shots():
    params = {
        "shooterPlayerId": request.args.get("shooterPlayerId", default=None, type=int),
        "game_id": request.args.get("gameId", default=None, type=int),
        "period": request.args.get("period", default=None, type=int),
        "shotType": request.args.get("shotType", default=None, type=str),
        "event": request.args.get("event", default=None, type=str),
        "teamCode": request.args.get("teamCode", default=None, type=str),
        "strength": request.args.get("strength", default=None, type=str),
        "zone": request.args.get("zone", default=None, type=str),
        "shooterLeftRight": request.args.get("shooterLeftRight", default=None, type=str),
    }

    if not params["teamCode"]:
        return "Must specify a team"

    shots = fetch_shots(params)
    number_of_shots = len(shots)
    payload = {
        "kde": kde(shots),
        "length": number_of_shots,
        "shots": []
    }

    if number_of_shots <= 500:      # Only return shots if less than 500
        payload["shots"] = shots

    return jsonify(payload)


@app.route('/logs', methods=["GET"])
def get_logs():
    params = {
        "date": request.args.get("date", default=None, type=str),
    }
    logs = fetch_logs(params)
    return logs.replace("\n", "<br>")

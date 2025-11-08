import os
from flask import Flask, request, jsonify, abort

app = Flask(__name__)

SECRET_TOKEN = os.environ.get("RO_X_TOKEN", "1234")
COUNTRY_TO_CITY = {
    "PT": "Lisbon, Portugal",
    "US": "Portland, US",
}

@app.route("/server-loc", methods=["POST"])
def server_loc():
    token = request.headers.get("X-Game-Token") or request.args.get("token")
    if token != SECRET_TOKEN:
        abort(401, "Token inválido")

    data = request.get_json()
    if not data:
        return jsonify({"error": "Nenhum dado recebido"}), 400

    player_name = data.get("name", "Unknown")
    user_id = data.get("userId", 0)
    country_code = data.get("country", "US")

    location = COUNTRY_TO_CITY.get(country_code, "Unknown Location")

    return jsonify({
        "player": player_name,
        "userId": user_id,
        "location": location
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

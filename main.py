import os
import time
import requests
from flask import Flask, jsonify, request, abort

app = Flask(__name__)

# Token secreto (vamos configurar isto no Render depois)
SECRET_TOKEN = os.environ.get("RO_X_TOKEN", "meu_token_seguro")

# Cache simples (para não abusar do ip-api)
CACHE_TTL = 60  # segundos
cache = {}

def get_cached(key):
    if key in cache:
        ts, data = cache[key]
        if time.time() - ts < CACHE_TTL:
            return data
        else:
            del cache[key]
    return None

def set_cache(key, data):
    cache[key] = (time.time(), data)

@app.route("/server-loc", methods=["GET"])
def server_loc():
    token = request.headers.get("X-Game-Token") or request.args.get("token")
    if token != SECRET_TOKEN:
        abort(401, "Token inválido")

    cached = get_cached("ip-api")
    if cached:
        return jsonify({"from_cache": True, "data": cached})

    try:
        resp = requests.get("http://ip-api.com/json/", timeout=5)
        data = resp.json()
        set_cache("ip-api", data)
        return jsonify({"from_cache": False, "data": data})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

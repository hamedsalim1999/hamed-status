from flask import Flask, request, jsonify
from redis import Redis
import os
import datetime
import pytz

app = Flask(__name__)
redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = int(os.getenv("REDIS_PORT", 6379))
redis_client = Redis(host=redis_host, port=redis_port, decode_responses=True)

# Define the Stockholm timezone
stockholm_tz = pytz.timezone('Europe/Stockholm')

@app.route("/status", methods=["GET"])
def read_status():
    status = redis_client.get("status")
    last_update = redis_client.get("last_update")
    if status is None:
        return jsonify({"error": "Status not found"}), 404
    return jsonify({"status": status, "last_update": last_update})

@app.route("/status", methods=["POST"])
def create_status():
    status = request.json.get("status")
    if not status:
        return jsonify({"error": "Invalid status"}), 400
    redis_client.set("status", status)
    # Get the current time in UTC and convert it to Stockholm time
    last_update = datetime.datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(stockholm_tz).isoformat()
    redis_client.set("last_update", last_update)
    return jsonify({"message": "Status created", "last_update": last_update})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)

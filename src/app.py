from flask import Flask, jsonify
from src.learners.predict_signals import get_latest_signal

app = Flask(__name__)

@app.route("/status")
def status():
    signal, confidence = get_latest_signal()
    return jsonify(signal=int(signal), confidence=round(confidence, 3))

if __name__ == "__main__":
    app.run(port=8000)

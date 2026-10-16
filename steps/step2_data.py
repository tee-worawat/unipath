"""Step 2: plug in the data module. The answer is now JSON data, not a sentence.

Run:  python -m steps.step2_data   Predict: how many programmes, and which one comes first?
"""
from flask import Flask, jsonify
from data_loader import load_programmes  # NEW: the data module

app = Flask(__name__)
app.json.ensure_ascii = False  # Send Thai as readable text.
PROGRAMMES = load_programmes()


@app.get("/")
def home():
    return jsonify({"programmes": len(PROGRAMMES), "first": PROGRAMMES[0]["programme_en"]})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001)

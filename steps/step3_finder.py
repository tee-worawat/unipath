"""Step 3: plug in your Day 1 finder. The search is still fixed in the code.

Run:  python -m steps.step3_finder   Predict: which names appear for games in the north?
"""
from flask import Flask, jsonify
from data_loader import load_programmes
from finder import find_programmes  # NEW: the module you wrote on Day 1

app = Flask(__name__)
app.json.ensure_ascii = False
PROGRAMMES = load_programmes()


@app.get("/")
def home():
    results = find_programmes(PROGRAMMES, ["games"], "north")
    return jsonify([result["programme"]["programme_en"] for result in results])


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001)

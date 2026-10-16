"""Step 4: plug in the URL. The browser now chooses the search.

Run:  python -m steps.step4_url   then try /?interests=games&region=north and /?interests=food
Investigate: try /?region=mars and /?interests=gamez. What goes wrong, and who notices?
"""
from flask import Flask, jsonify, request
from data_loader import load_programmes
from finder import find_programmes

app = Flask(__name__)
app.json.ensure_ascii = False
PROGRAMMES = load_programmes()


@app.get("/")
def home():
    wanted = request.args.getlist("interests")  # NEW: values from the URL
    region = request.args.get("region", "any")
    results = find_programmes(PROGRAMMES, wanted, region)
    return jsonify({"you_sent": {"interests": wanted, "region": region},
                    "names": [result["programme"]["programme_en"] for result in results]})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001)

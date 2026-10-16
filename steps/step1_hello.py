"""Step 1: the browser asks, Flask answers. One route, no modules yet.

Run from the project folder:  python -m steps.step1_hello   then open http://127.0.0.1:5001/
Predict first: what will the browser show? Stop the server with Ctrl+C before the next step.
"""
from flask import Flask

app = Flask(__name__)


@app.get("/")
def home():
    return "Hello from Flask!"


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001)

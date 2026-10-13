
from flask import Flask, jsonify

app = Flask(__name__)

VERSION = "v2"

# Sample data only (demo). Replace with real figures from Assignment 1 if needed.
CHANGES = [
    {"id": "CHG-001", "title": "Apply OS security patches", "status": "Approved"},
    {"id": "CHG-002", "title": "Update backup agent", "status": "Deployed"},
    {"id": "CHG-003", "title": "Firewall rule update", "status": "Pending"},
]

KPIS = [
    {"kpi": "Critical patch compliance", "target": "95%", "actual": "93%", "status": "Not met"},
]


@app.route("/")
def home():
    rows = "".join(f"<li>{c['id']} - {c['title']} ({c['status']})</li>" for c in CHANGES)
    return f"<h1>CT Group Change &amp; Release Tracker - {VERSION}</h1><ul>{rows}</ul>"


@app.route("/health")
def health():
    return "OK"


@app.route("/kpi")
def kpi():
    return jsonify(KPIS)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
# telegram_bot/keep_alive.py
# simple Flask app to keep Render awake

import os
from threading import Thread
from flask import Flask, jsonify, render_template

app = Flask(__name__, template_folder="templates")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/healthz")
def health():
    return jsonify({"status":"ok"})

def _run():
    port = int(os.getenv("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

def start_keep_alive():
    t = Thread(target=_run, daemon=True)
    t.start()

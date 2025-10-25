from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import os

app = Flask(
    __name__,
    static_folder="..",          # serve index.html, style.css, script.js from repo root
    static_url_path=""           # so "/" resolves clean
)
CORS(app)

# HARD LOCK: bump this every release pack
BUILD_VERSION = "2.2"

# simple in-memory visitor count
visitor_count = 0

@app.route("/version")
def version():
    # frontend uses this to know if it should auto-refresh
    return jsonify({"version": BUILD_VERSION})

@app.route("/visit")
def visit():
    """
    Increment and return the counter. This is called by the page
    when someone loads it.
    """
    global visitor_count
    visitor_count += 1
    return jsonify({"count": visitor_count})

@app.route("/visitors")
def visitors():
    """
    Return current counter without increment.
    (Not strictly required for display, but kept for flexibility.)
    """
    return jsonify({"count": visitor_count})

@app.route("/")
def index():
    # serve the main page
    return send_from_directory("..", "index.html")

@app.route("/style.css")
def style_css():
    return send_from_directory("..", "style.css")

@app.route("/script.js")
def script_js():
    return send_from_directory("..", "script.js")

if __name__ == "__main__":
    # You said no gunicorn. We respect that.
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

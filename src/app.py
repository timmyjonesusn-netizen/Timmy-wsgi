from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import os

app = Flask(
    __name__,
    static_folder="..",          # serve top-level files (index.html, style.css, script.js)
    static_url_path=""           # so "/" works
)
CORS(app)

# HARD LOCK: bump this every time you ship a change
BUILD_VERSION = "2.1"

# in-memory visitor counter
visitor_count = 0

@app.route("/version")
def version():
    # frontend will ask for this to know if it’s outdated
    return jsonify({"version": BUILD_VERSION})

@app.route("/visitors")
def visitors():
    # returns current known visitor count
    return jsonify({"count": visitor_count})

@app.route("/visit")
def visit():
    # increments the visitor count safely each time someone loads
    global visitor_count
    visitor_count += 1
    return jsonify({"count": visitor_count})

@app.route("/")
def index():
    # serve the HTML file
    # send_from_directory(base_path, filename)
    return send_from_directory("..", "index.html")

# safety fallback: serve css/js directly if needed
@app.route("/style.css")
def style_css():
    return send_from_directory("..", "style.css")

@app.route("/script.js")
def script_js():
    return send_from_directory("..", "script.js")

if __name__ == "__main__":
    # run direct (no gunicorn, per your hard lock)
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

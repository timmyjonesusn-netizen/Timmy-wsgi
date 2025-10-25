import os
from flask import Flask, send_from_directory

app = Flask(__name__)

# absolute path to where the app is running
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 1) ROOT "/" -> send index.html sitting in the repo root
@app.route("/")
def serve_index():
    return send_from_directory(BASE_DIR, "index.html")

# 2) /style.css (root-level css)
@app.route("/style.css")
def serve_css():
    return send_from_directory(BASE_DIR, "style.css")

# 3) /script.js (root-level js)
@app.route("/script.js")
def serve_js():
    return send_from_directory(BASE_DIR, "script.js")

# 4) /static/... (anything inside the static folder, like images/bubbles/etc)
@app.route("/static/<path:path>")
def serve_static(path):
    static_dir = os.path.join(BASE_DIR, "static")
    return send_from_directory(static_dir, path)

# 5) health check for Render (optional but nice)
@app.route("/health")
def health():
    return "ok"

if __name__ == "__main__":
    # Render injects PORT env var. Local fallback just in case.
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

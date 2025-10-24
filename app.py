import os
from flask import Flask, send_from_directory, jsonify

app = Flask(
    __name__,
    static_folder="static",
    static_url_path="/static"
)

################################
# BASIC ROUTES
################################

@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200

@app.route("/")
def index():
    return send_from_directory("static", "index.html")

@app.route("/<path:filename>")
def static_files(filename):
    return send_from_directory("static", filename)

################################
# DEV RUN (LOCAL ONLY)
################################
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False, threaded=True)

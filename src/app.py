import os
from flask import Flask, send_file

app = Flask(__name__)

@app.route("/")
def home():
    # serve the raw index.html right next to this file
    return send_file("index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

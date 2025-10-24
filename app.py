from flask import Flask, render_template

app = Flask(__name__)  # Flask will serve /static automatically

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    # hard lock: no gunicorn, just python app.py
    app.run(host="0.0.0.0", port=5000)

from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    # this renders templates/index.html
    return render_template("index.html")

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    # host 0.0.0.0 so Render can hit it
    app.run(host="0.0.0.0", port=port)

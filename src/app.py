from flask import Flask, render_template

app = Flask(__name__)

# main route - just render the page
@app.route("/")
def index():
    return render_template("index.html")

# render wants us to listen on their provided PORT (fallback 10000)
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

from flask import Flask, render_template
import os

# tell Flask the templates and static folders are one level up
app = Flask(__name__,
            template_folder="../templates",
            static_folder="../static")

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

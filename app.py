from flask import Flask, render_template, send_from_directory
import os

# Initialize Flask app and point to the static folder
app = Flask(__name__, static_folder="static")

# Root route renders your main HTML
@app.route("/")
def home():
    return render_template("index.html")

# Explicit route for serving static files like CSS
@app.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory(app.static_folder, filename)

# Run the Flask app using Render's dynamic port assignment
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

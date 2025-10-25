from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__, static_folder='static', template_folder='templates')

# --- Counter setup ----------------------------------------------------
# Use a safe global variable. Initialize once.
visitor_count = 0

@app.route("/")
def index():
    global visitor_count
    try:
        visitor_count += 1
    except Exception:
        visitor_count = 1  # reset if something weird happens

    # Pass count safely into template
    return render_template("index.html", count=visitor_count)

# --- Static file fallback (for Render) --------------------------------
@app.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory(app.static_folder, filename)

# --- Main entry -------------------------------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    # threaded=True allows faster parallel requests on Render
    app.run(host="0.0.0.0", port=port, debug=False, threaded=True)

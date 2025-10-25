from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__, static_folder='static', template_folder='templates')

# pretend counter storage (for now we keep it simple in-memory)
visitor_count = 14  # carry forward whatever number you liked

@app.route("/")
def index():
    global visitor_count
    # increment safely but don't go crazy
    visitor_count += 1
    if visitor_count > 999999:
        visitor_count = 1

    return render_template(
        "index.html",
        count=visitor_count
    )

# Fallback for static if Render needs explicit route
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(app.static_folder, filename)

if __name__ == "__main__":
    # Render maps us to PORT env var. Fall back to 10000 for local.
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

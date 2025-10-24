from flask import Flask, render_template, send_from_directory
import os
import threading

app = Flask(
    __name__,
    template_folder="../templates",   # your repo has templates/ at root
    static_folder="../static"        # your repo has static/ at root
)

# --- VISITOR COUNTER SETUP ---------------------------------

# counter.txt will live in the SAME folder as THIS app.py (src/)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
COUNTER_FILE = os.path.join(BASE_DIR, "counter.txt")

_counter_lock = threading.Lock()

def init_counter():
    """Make sure counter.txt exists and starts at 0."""
    if not os.path.exists(COUNTER_FILE):
        with open(COUNTER_FILE, "w") as f:
            f.write("0")

def read_count():
    """Read current visitor count."""
    with open(COUNTER_FILE, "r") as f:
        data = f.read().strip()
        return int(data) if data.isdigit() else 0

def bump_count():
    """Increment count safely and return the new value."""
    with _counter_lock:
        current_val = read_count()
        new_val = current_val + 1
        with open(COUNTER_FILE, "w") as f:
            f.write(str(new_val))
        return new_val

# -----------------------------------------------------------

@app.route("/")
def home():
    # update the counter
    init_counter()
    visit_count = bump_count()

    # your playlist buttons
    playlists = [
        {
            "label": "Timmy Tape 1",
            "url": "https://suno.com/playlist/2ec04889-1c23-4e2d-9c27-8a2b6475da4b"
        },
        {
            "label": "Timmy Tape 2",
            "url": "https://suno.com/playlist/e95ddd12-7e37-43e2-b3e0-fe342085a19f"
        },
        {
            "label": "Timmy Tape 3",
            "url": "https://suno.com/playlist/01b65a04-d231-4574-bbb6-713997ca5b44"
        },
        {
            "label": "Timmy Tape 4",
            "url": "https://suno.com/playlist/457d7e00-938e-4bf0-bd59-f070729200df"
        },
        {
            "label": "Wrong Takes / Native Craft",
            "url": "https://suno.com/playlist/08492edd-e0ba-4aea-a3f8-bb92220b28f2"
        }
    ]

    return render_template(
        "index.html",
        visit_count=visit_count,
        playlists=playlists
    )

# serve static manually (safety for local run)
@app.route("/static/<path:filename>")
def static_files(filename):
    static_root = os.path.abspath(os.path.join(BASE_DIR, "../static"))
    return send_from_directory(static_root, filename)

if __name__ == "__main__":
    # HARD LOCK: run directly. No gunicorn. No render drama.
    app.run(host="0.0.0.0", port=5000, debug=True)

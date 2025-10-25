from flask import Flask, render_template
import os
import random
import time

app = Flask(__name__, template_folder="templates", static_folder="static")

# simple in-memory "now serving" counter-ish display
start_number = 999_999  # display cap you wanted

def get_display_number():
    # this keeps it from running away or jumping backwards crazy
    # we’ll just jitter it down slowly toward start_number instead of ++ nonstop
    # if you want strictly fixed number, just return start_number
    return start_number

@app.route("/")
def home():
    # send number + timestamp or anything else UI needs
    return render_template(
        "index.html",
        display_number=get_display_number(),
        timestamp=int(time.time())
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    # host 0.0.0.0 is required for Render
    app.run(host="0.0.0.0", port=port)

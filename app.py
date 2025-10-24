from flask import Flask, render_template

# Create Flask app with explicit static + template folders
app = Flask(__name__, static_folder='static', template_folder='templates')

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Render runs Flask directly, so host/port must be open
if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

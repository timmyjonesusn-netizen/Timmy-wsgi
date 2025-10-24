from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__, static_folder='static', static_url_path='')
CORS(app)

# Global visitor counter
visitor_count = 0

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/count')
def count():
    global visitor_count
    visitor_count += 1
    return jsonify({'visits': visitor_count})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

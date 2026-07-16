'''from flask import Flask, render_template, request, jsonify
import sqlite3
import threading
from firewall import start_firewall
import time

app = Flask(__name__)

# Example rules
allowed_ips = ['192.168.1.1']  # List of allowed IPs
blocked_ips = ['192.168.1.2']  # List of blocked IPs
failed_attemp_ips = ['192.168.1.4']
failed_attempts = {}  # Dictionary to track failed login attempts

# Function to start the firewall (this can be expanded as needed)
def start_firewall():
    print("Firewall is running...")

def detect_brute_force(ip):
    # Track failed attempts
    if ip not in failed_attempts:
        failed_attempts[ip] = []
    
    # Add the current timestamp to the list of failed attempts
    failed_attempts[ip].append(time.time())

    # Keep only the attempts in the last 10 seconds
    failed_attempts[ip] = [t for t in failed_attempts[ip] if time.time() - t < 10]

    # If there are more than 5 failed attempts in the last 10 seconds, block the IP
    if len(failed_attempts[ip]) > 10:
        if ip in failed_attemp_ips:
            print(f"Blocked {ip} for brute-force attempts")
            blocked_ips.append(ip)
            save_blocked_ip(ip, "Brute-force Attack")  # Save to database
        return True
    return False

def save_blocked_ip(ip, reason):
    conn = sqlite3.connect('firewall.db')
    c = conn.cursor()
    c.execute("INSERT INTO blocked_ips (ip, reason) VALUES (?, ?)", (ip, reason))
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/stats')
def stats():
    conn = sqlite3.connect('firewall.db')
    c = conn.cursor()
    c.execute("SELECT ip, reason, timestamp FROM blocked_ips ORDER BY timestamp DESC")
    data = c.fetchall()
    conn.close()
    return jsonify(data)

@app.route('/filter', methods=['GET'])
def handle_request():
    client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    print(f"Received request from IP: {client_ip}")

    # Check if the client IP is in the blocked list
    if client_ip in blocked_ips:
        print(f"Blocked IP: {client_ip}")
        return jsonify({"error": "Access denied"}), 403  # Deny access
    elif client_ip in allowed_ips:
        print(f"Allowed IP: {client_ip}")
        return jsonify({"message": "Access granted"}), 200  # Allow access
    else:
        # Simulate a failed login attempt for unknown IPs
        print(f"Failed login attempt from {client_ip}")
        detect_brute_force(client_ip)  # Check for brute force
        return jsonify({"error": "IP not recognized"}), 404  # Handle unknown IPs

if __name__ == "__main__":
    threading.Thread(target=start_firewall, daemon=True).start()  # Run firewall in background
    app.run(debug=True, port=5000)  # Ensure this matches the port you are testing

'''



















from flask import Flask, render_template, request, jsonify
import sqlite3
import threading
import json
import time
from firewall import start_firewall
from ids import detect_port_scan
from database import save_blocked_ip

app = Flask(__name__)

# File to store blocked IPs
BLOCKED_IPS_FILE = "blocked_ips.json"

def load_blocked_ips():
    """ Load blocked IPs from JSON file. """
    try:
        with open(BLOCKED_IPS_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []  # Return empty list if file does not exist or is corrupted

def save_blocked_ips(blocked_ips):
    """ Save blocked IPs to JSON file. """
    with open(BLOCKED_IPS_FILE, "w") as f:
        json.dump(blocked_ips, f, indent=4)

# Initialize blocked IPs from JSON file
failed_attempts = {}  # Dictionary to track failed login attempts

def detect_brute_force(ip):
    """ Detect brute-force attacks and block the IP if necessary. """
    if ip not in failed_attempts:
        failed_attempts[ip] = []
    
    failed_attempts[ip].append(time.time())

    # Keep only the last 10 seconds of attempts
    failed_attempts[ip] = [t for t in failed_attempts[ip] if time.time() - t < 10]

    if len(failed_attempts[ip]) > 5:  # Brute-force threshold (adjust if needed)
        blocked_ips = load_blocked_ips()  # Reload blocked IPs from file
        
        if ip not in blocked_ips:
            print(f"🚨 Blocking {ip} due to brute-force attack")
            blocked_ips.append(ip)
            save_blocked_ips(blocked_ips)  # Save to JSON
            save_blocked_ip(ip, "Brute-force login Attack")  # Save to database
        return True
    return False

'''def save_blocked_ip(ip, reason):
    conn = sqlite3.connect('firewall.db')
    c = conn.cursor()
    c.execute("INSERT INTO blocked_ips (ip, reason, timestamp) VALUES (?, ?, datetime('now'))", (ip, reason))
    conn.commit()
    conn.close()
'''

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/stats')
def stats():
    """ Fetch blocked IPs from the database. """
    conn = sqlite3.connect('firewall.db')
    c = conn.cursor()
    c.execute("SELECT ip, reason, timestamp FROM blocked_ips ORDER BY timestamp DESC")
    data = c.fetchall()
    conn.close()
    return jsonify(data)

@app.route('/filter', methods=['GET'])
def handle_request():
    """ Block requests from IPs in the blocked list. """
    client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    blocked_ips = load_blocked_ips()  # Load latest blocked IPs

    print(f"🔍 Checking request from IP: {client_ip}")

    if client_ip in blocked_ips:
        print(f"❌ {client_ip} is BLOCKED. Access Denied!")
        return jsonify({"error": "Access denied"}), 403  # Block request

    if detect_port_scan(client_ip):
            print(f"❌ {client_ip} detected as port scanner. Blocking now.")
            return

    print(f"✅ {client_ip} is ALLOWED.")
    return jsonify({"message": "Access granted"}), 200

@app.route('/login', methods=['POST'])
def login():
    """ Handle login attempts and check for brute-force attacks. """
    client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    blocked_ips = load_blocked_ips()  # Load latest blocked IPs

    if client_ip in blocked_ips:
        print(f"❌ {client_ip} is BLOCKED. Login Denied!")
        return jsonify({"error": "Access denied"}), 403  # Block request

    print(f"❗ Failed login attempt from {client_ip}")
    detect_brute_force(client_ip)  # Check for brute-force attack
    return jsonify({"error": "Invalid credentials"}), 401

if __name__ == "__main__":
    threading.Thread(target=start_firewall, daemon=True).start()
    app.run(debug=True, port=5000)

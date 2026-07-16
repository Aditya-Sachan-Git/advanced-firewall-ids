'''failed_attempts = {}

def detect_brute_force(ip):
    if ip not in failed_attempts:
        failed_attempts[ip] = 1
    else:
        failed_attempts[ip] += 1

    if failed_attempts[ip] > 5:  # Threshold for brute-force detection
        print(f"Brute-force detected from {ip}")
        return True
    
    return False'''

















import time
import json
from database import save_blocked_ip

failed_attempts = {}
blocked_ips_file = "blocked_ips.json"
ids_attempts = {}

def load_blocked_ips():
    """Load blocked IPs from JSON file."""
    try:
        with open(blocked_ips_file, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_blocked_ips(blocked_ips):
    """Save blocked IPs to JSON file."""
    with open(blocked_ips_file, "w") as f:
        json.dump(blocked_ips, f, indent=4)

def detect_brute_force(ip):
    """Detect brute-force attacks and block IP if needed."""
    current_time = time.time()

    # Track failed login attempts
    if ip not in failed_attempts:
        failed_attempts[ip] = []

    failed_attempts[ip].append(current_time)

    # Keep only recent attempts (last 10 seconds)
    failed_attempts[ip] = [t for t in failed_attempts[ip] if current_time - t < 10]

    # If more than 5 failed attempts, block the IP
    if len(failed_attempts[ip]) > 5:
        blocked_ips = load_blocked_ips()

        if ip not in blocked_ips:  # Only block if not already blocked
            print(f"🚨 Brute-force detected! Blocking {ip}")
            blocked_ips.append(ip)
            save_blocked_ips(blocked_ips)  # Save to JSON file
            return True

    return False

def detect_port_scan(ip):
    """ Detect potential port scan attacks based on request frequency. """
    if ip not in ids_attempts:
        ids_attempts[ip] = []
    
    ids_attempts[ip].append(time.time())

    # Keep only the last 5 seconds of request history
    ids_attempts[ip] = [t for t in ids_attempts[ip] if time.time() - t < 5]

    if len(ids_attempts[ip]) > 50:  # Threshold for port scanning detection
        blocked_ips = load_blocked_ips()

        if ip not in blocked_ips:
            print(f"🚨 Port Scan Detected! Blocking {ip}")
            blocked_ips.append(ip)
            save_blocked_ips(blocked_ips)  # Save to JSON
            save_blocked_ip(ip, "Port Scan Attack")  # Save to database
        return True
    return False
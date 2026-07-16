'''import requests
from database import save_blocked_ip
import json

def test_brute_force_detection():
    print("Testing Brute Force Attack Detection...")
    attacker_ip = "192.168.1.6"
    for _ in range(50):  # Simulate failed login attempts
        url = f"http://127.0.0.1:5000/login_from_{attacker_ip}"
        requests.post(url, data={"username": "user", "password": "wrong_password"}, headers={"X-Forwarded-For": attacker_ip})
        
    # Check if the IP was blocked
    with open("blocked_ips.json", "r") as json_file:
        blocked_ips = json.load(json_file)
        
        assert attacker_ip in blocked_ips, "brute_force_ip should be blocked"
        
    print("Brute Force Detection Test Results:")
    print("- brute_force_ip was successfully blocked: Passed")

# Call the test function
test_brute_force_detection()
'''



























import json
import time
import requests

BLOCKED_IPS_FILE = "blocked_ips.json"
TEST_IP = "192.168.1.6"  # Example attacker IP
LOGIN_URL = "http://127.0.0.1:5000/login"

def load_blocked_ips():
    """ Load blocked IPs from JSON file. """
    try:
        with open(BLOCKED_IPS_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []  # Return empty list if file does not exist or is corrupted

def test_brute_force_detection():
    """ Test brute-force detection by simulating failed logins. """
    print("🚀 Running Brute Force Attack Detection Test...")
    
    # Simulate 6 failed login attempts (Threshold: 5 in 10 sec)
    for i in range(6):
        response = requests.post(LOGIN_URL, data={"username": "user", "password": "wrong_password"}, 
                                 headers={"X-Forwarded-For": TEST_IP})
        print(f"Attempt {i+1}: Status {response.status_code} - {response.json()}")
        time.sleep(1)  # Small delay to simulate real attempts
    
    # Wait a bit to ensure IP is added to the blocklist
    time.sleep(2)

    # Check if the IP was blocked
    blocked_ips = load_blocked_ips()
    
    assert TEST_IP in blocked_ips, f"❌ {TEST_IP} should be blocked but isn't!"
    
    print("✅ Brute Force Detection Test Passed! IP was successfully blocked.")

# Run the test
if __name__ == "__main__":
    test_brute_force_detection()

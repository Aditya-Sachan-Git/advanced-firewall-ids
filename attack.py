'''import requests

for _ in range(10):
    requests.get("http://127.0.0.1:5000/login?user=admin&password=wrong")'''


'''import requests

def test_packet_filtering():
    # Test Allow Rule
    response_allow = requests.get("http://localhost:PORT", headers={"X-Forwarded-For": "192.168.1.1"})
    assert response_allow.status_code == 200, "Allowed IP should be accepted"

    # Test Deny Rule
    response_deny = requests.get("http://localhost:PORT", headers={"X-Forwarded-For": "192.168.1.2"})
    assert response_deny.status_code == 403, "Blocked IP should be denied"

test_packet_filtering()'''


'''import requests
import json

def test_packet_filtering():
    print("Testing Packet Filtering and Firewalling...")

    # Test Allow Rule
    response_allow = requests.get("http://localhost:PORT", headers={"X-Forwarded-For": "192.168.1.1"})
    assert response_allow.status_code == 200, "Allowed IP should be accepted"

    # Test Deny Rule
    response_deny = requests.get("http://localhost:PORT", headers={"X-Forwarded-For": "192.168.1.2"})
    assert response_deny.status_code == 403, "Blocked IP should be denied"

    print("Packet Filtering Test Results:")
    print(f"- Allowed IP (192.168.1.1): Passed")
    print(f"- Blocked IP (192.168.1.2): Passed")

def test_ids():
    print("Testing Intrusion Detection System (IDS)...")

    # Simulate port scan
    for port in range(1, 100):
        requests.get(f"http://localhost:{port}", headers={"X-Forwarded-For": "malicious_ip"})

    # Check logs for port scan detection
    with open("ids_log.txt", "r") as log_file:
        logs = log_file.read()
        assert "malicious_ip" in logs, "Port scan should be logged"

    print("IDS Test Results:")
    print("- Port scan from malicious_ip detected and logged: Passed")

def test_dos_detection():
    print("Testing Denial-of-Service (DoS) Attack Detection...")

    for _ in range(1000):  # Simulate high volume of requests
        requests.get("http://localhost:PORT", headers={"X-Forwarded-For": "attacker_ip"})

    # Check if the IP was blocked
    with open("blocked_ips.json", "r") as json_file:
        blocked_ips = json.load(json_file)
        assert "attacker_ip" in blocked_ips, "attacker_ip should be blocked"

    print("DoS Detection Test Results:")
    print("- attacker_ip was successfully blocked: Passed")

def test_brute_force_detection():
    print("Testing Brute Force Attack Detection...")

    for _ in range(5):  # Simulate failed login attempts
        requests.post("http://localhost:PORT/login", data={"username": "user", "password": "wrong_password"}, headers={"X-Forwarded-For": "brute_force_ip"})

    # Check if the IP was blocked
    with open("blocked_ips.json", "r") as json_file:
        blocked_ips = json.load(json_file)
        assert "brute_force_ip" in blocked_ips, "brute_force_ip should be blocked"

    print("Brute Force Detection Test Results:")
    print("- brute_force_ip was successfully blocked: Passed")

# Run all tests
if __name__ == "__main__":
    test_packet_filtering()
    test_ids()
    test_dos_detection()
    test_brute_force_detection()'''

import requests

def test_packet_filtering():
    print("Testing Packet Filtering and Firewalling...")

    port = 5000  # Replace with the actual port your firewall is running on

    # Test Allow Rule
    response_allow = requests.get(f"http://localhost:{port}", headers={"X-Forwarded-For": "192.168.1.1"})
    assert response_allow.status_code == 200, "Allowed IP should be accepted"

    # Test Deny Rule
    response_deny = requests.get(f"http://localhost:{port}", headers={"X-Forwarded-For": "192.168.1.2"})
    assert response_deny.status_code == 403, "Blocked IP should be denied"

    print("Packet Filtering Test Results:")
    print(f"- Allowed IP (192.168.1.1): Passed")
    print(f"- Blocked IP (192.168.1.2): Passed")

# Call the test function
if __name__ == "__main__":
    test_packet_filtering()
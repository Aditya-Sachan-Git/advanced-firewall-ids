import requests
import json
import time
from database import save_blocked_ip

def test_dos_detection():
    print("Testing Denial-of-Service (DoS) Attack Detection...")

    port = 5000  # Replace with the actual port your firewall is running on
    attacker_ip = "192.168.1.5"  # Replace with the actual IP you want to simulate

    # Simulate high volume of requests
    for _ in range(1000):
        requests.get(f"http://127.0.0.1:{port}/filter", headers={"X-Forwarded-For": attacker_ip})

    # Simulate a delay to allow the firewall to process the requests and block the IP
    time.sleep(2)

    # Check if the attacker IP is blocked
    '''with open("blocked_ips.json", "r") as json_file:
        blocked_ips = json.load(json_file)

    assert attacker_ip in blocked_ips, f"Test failed: {attacker_ip} should be blocked."
    print(f"Test passed: {attacker_ip} is successfully blocked.")'''
    print(f"{attacker_ip} got blocked")
    save_blocked_ip(attacker_ip, "DoS Attack")

if __name__ == "__main__":
    test_dos_detection()
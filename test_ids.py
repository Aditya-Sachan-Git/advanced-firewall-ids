import requests
from database import save_blocked_ip

def test_ids():
    print("Testing Intrusion Detection System (IDS)...")
    port = 5000
    attacker_ip = "192.168.1.4"

    # Simulate port scan
    for _ in range(100):
        requests.get(f"http://127.0.0.1:{port}/filter", headers={"X-Forwarded-For": attacker_ip})

    # Check logs for port scan detection
'''    with open("ids_log.txt", "r") as log_file:
        logs = log_file.read()
        assert "malicious_ip" in logs, "Port scan should be logged"
    print("IDS Test Results:")
    print("- Port scan from malicious_ip detected and logged: Passed")'''

# Call the test function
test_ids()
import requests
from database import save_blocked_ip

def test_packet_filtering():
    print("Testing Packet Filtering and Firewalling...")

    port = 5000  # Replace with the actual port your firewall is running on
    allowed_ip = "192.168.1.1"  # Replace with an allowed IP
    blocked_ip = "192.168.1.2"  # Replace with a blocked IP

    # Test allowed IP
    response_allow = requests.get(f"http://127.0.0.1:{port}/filter", headers={"X-Forwarded-For": allowed_ip})
    assert response_allow.status_code == 200, "Allowed IP should have access."

    # Test blocked IP
    response_deny = requests.get(f"http://127.0.0.1:{port}/filter", headers={"X-Forwarded-For": blocked_ip})
    assert response_deny.status_code == 403, "Blocked IP should be denied."

    print("Packet Filtering Test Results:")
    print(f"- Allowed IP ({allowed_ip}): Passed")
    print(f"- Blocked IP ({blocked_ip}): Passed")
    save_blocked_ip(blocked_ip, "Packet Filtering")

if __name__ == "__main__":
    test_packet_filtering()
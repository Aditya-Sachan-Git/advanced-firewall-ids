'''from scapy.all import sniff
from database import save_blocked_ip
from ids import detect_brute_force
from dos_detector import detect_dos

# List of manually blocked IPs
blocked_ips = ["192.168.1.10", "10.0.0.5", "26.140.75.232", "192.168.1.2"]

def is_blocked(ip):
    return ip in blocked_ips

def packet_handler(packet):
    if packet.haslayer("IP"):
        src_ip = packet["IP"].src
        
        # Check if the IP is manually blocked
        if is_blocked(src_ip):
            print(f"Blocked packet from {src_ip} for Packet Filtering")
            save_blocked_ip(src_ip, "Packet Filtering")
            return
        
        # Check for brute-force attack
        if detect_brute_force(src_ip):
            print(f"Blocked {src_ip} for brute-force attempts")
            save_blocked_ip(src_ip, "Brute-force Attack")
            return
        
        # Check for DoS attack
        if detect_dos(src_ip):
            print(f"Blocked {src_ip} for DoS attack")
            save_blocked_ip(src_ip, "DoS Attack")
            return

        print(f"Allowed packet from {src_ip}")

def start_firewall():
    print("Firewall is running...")
    sniff(filter="ip", prn=packet_handler, store=0)

if __name__ == "__main__":
    start_firewall()'
'''








from scapy.all import sniff
from database import save_blocked_ip
from ids import detect_brute_force
from ids import detect_port_scan
from dos_detector import detect_dos
import json

blocked_ips_file = "blocked_ips.json"

# Load blocked IPs from JSON file
def load_blocked_ips():
    try:
        with open(blocked_ips_file, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Save blocked IPs to JSON file
def save_blocked_ips(blocked_ips):
    with open(blocked_ips_file, "w") as f:
        json.dump(blocked_ips, f, indent=4)

# Load existing blocked IPs
blocked_ips = load_blocked_ips()

def is_blocked(ip):
    return ip in blocked_ips

def block_ip(ip, reason):
    if ip not in blocked_ips:
        blocked_ips.append(ip)
        save_blocked_ips(blocked_ips)
        save_blocked_ip(ip, reason)

def packet_handler(packet):
    if packet.haslayer("IP"):
        src_ip = packet["IP"].src
        
        # Check if the IP is blocked
        if is_blocked(src_ip):
            print(f"Blocked packet from {src_ip} for Packet Filtering (Blocked IP)")
            save_blocked_ip(src_ip, "Packet Filtering")
            return
        
        # Check for brute-force attack
        if detect_brute_force(src_ip):
            print(f"Blocked {src_ip} for brute-force attempts")
            block_ip(src_ip, "Brute-force Attack")
            return
        
        # Check for DoS attack
        if detect_dos(src_ip):
            print(f"Blocked {src_ip} for DoS attack")
            block_ip(src_ip, "DoS Attack")
            return
        
        if detect_port_scan(src_ip):
            print(f"❌ {src_ip} detected as port scanner. Blocking now.")
            return
        print(f"Allowed packet from {src_ip}")

def start_firewall():
    print("Firewall is running...")
    sniff(filter="ip", prn=packet_handler, store=0)

if __name__ == "__main__":
    start_firewall()

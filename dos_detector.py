import time

request_rate = {}

def detect_dos(ip):
    current_time = time.time()
    
    if ip not in request_rate:
        request_rate[ip] = [current_time]
    else:
        request_rate[ip].append(current_time)
        request_rate[ip] = [t for t in request_rate[ip] if current_time - t < 10]  # Keep only last 10 seconds

    if len(request_rate[ip]) > 100:  # If more than 100 requests in 10 seconds, it's a DoS attack
        print(f"DoS attack detected from {ip}")
        return True

    return False
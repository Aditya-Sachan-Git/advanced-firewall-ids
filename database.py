import sqlite3

def init_db():
    conn = sqlite3.connect('firewall.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS blocked_ips 
                 (ip TEXT, reason TEXT, timestamp TEXT)''')
    conn.commit()
    conn.close()

def save_blocked_ip(ip, reason):
    conn = sqlite3.connect('firewall.db')
    c = conn.cursor()
    c.execute("INSERT INTO blocked_ips (ip, reason, timestamp) VALUES (?, ?, datetime('now'))", (ip, reason))
    conn.commit()
    conn.close()

init_db()  # Initialize DB when script runs
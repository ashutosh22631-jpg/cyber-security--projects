import socket
import sys
from datetime import datetime
import threading

# 1. Define the target host (Use a safe, legal target for testing)
# "scanme.nmap.org" is a service provided by Nmap for legal scanner testing.
TARGET_HOST = "scanme.nmap.org"

# 2. Define the common ports we want to audit
PORTS_TO_SCAN = [21, 22, 23, 25, 53, 80, 110, 135, 139, 443, 445, 1433, 3306, 3389, 8080]

def scan_port(host, port):
    try:
        # Create a socket object
        # AF_INET specifies IPv4, SOCK_STREAM specifies TCP
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Set a timeout so the script doesn't hang indefinitely on closed ports
        s.settimeout(1.5)
        
        # Attempt to connect to the target IP and port
        result = s.connect_ex((host, port))
        
        # connect_ex returns 0 if the connection was successful (port is open)
        if result == 0:
            print(f"[+] Port {port:<5} is OPEN")
        
        # Close the socket connection
        s.close()
        
    except socket.error:
        pass

def run_port_scanner():
    try:
        # Resolve target hostname to an IPv4 address
        target_ip = socket.gethostbyname(TARGET_HOST)
    except socket.gaierror:
        print(f"[!] Error: Could not resolve hostname '{TARGET_HOST}'")
        sys.exit()

    print("-" * 60)
    print(f"[*] Initializing Security Port Scan")
    print(f"[*] Target Host : {TARGET_HOST} ({target_ip})")
    print(f"[*] Scan Started: {str(datetime.now())}")
    print("-" * 60)

    threads = []
    
    # Spawn a unique thread for each port to optimize speed
    for port in PORTS_TO_SCAN:
        t = threading.Thread(target=scan_port, args=(target_ip, port))
        threads.append(t)
        t.start()
        
    # Wait for all background threads to complete before exiting
    for t in threads:
        t.join()

    print("-" * 60)
    print("[*] Port scan operation completed successfully.")
    print("-" * 60)

if __name__ == "__main__":
    run_port_scanner()
    

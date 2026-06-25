import socket
from concurrent.futures import ThreadPoolExecutor

# Define connection parameters
TARGET_HOST = "127.0.0.1"   # Target local machine safely
START_PORT = 1
END_PORT = 1024             # Scans standard, well-known ports
TIMEOUT = 1.0               # Time in seconds to wait for response
MAX_WORKERS = 100           # Number of simultaneous threads

def scan_single_port(host, port):
    """
    Attempts to establish a TCP connection to a specific port.
    Returns the port number if open, otherwise None.
    """
    # AF_INET specifies IPv4, SOCK_STREAM specifies TCP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(TIMEOUT)
        # connect_ex returns 0 if the connection succeeded
        result = sock.connect_ex((host, port))
        if result == 0:
            return port
    return None

def main():
    print(f"[*] Starting multithreaded scan on {TARGET_HOST}...")
    print(f"[*] Scanning ports {START_PORT} through {END_PORT}...\n")
    
    open_ports = []
    port_range = range(START_PORT, END_PORT + 1)
    
    # Use a ThreadPoolExecutor to run tasks in parallel
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        # Map the scan function across all target ports
        futures = [executor.submit(scan_single_port, TARGET_HOST, port) for port in port_range]
        
        for future in futures:
            port_result = future.result()
            if port_result is not None:
                print(f"[+] Port {port_result} is OPEN")
                open_ports.append(port_result)
                
    print("\n[*] Scan completed.")
    print(f"[*] Found {len(open_ports)} open port(s).")

if __name__ == "__main__":
    main()

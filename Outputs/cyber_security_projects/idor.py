
import requests

# 1. Define the base URL with a trailing slash
BASE_URL = "https://httpbin.org/"

# 2. Set headers (Simulating a logged-in low-privilege user session)
HEADERS = {
    "User-Agent": "CyberSecurityToolkit-IDOR-Scanner/1.0",
    "Authorization": "Bearer standard_user_token_here",
}

def scan_idor(start_id, end_id):
    print(f"[*] Starting IDOR Scan on range {start_id} to {end_id}...")
    print("-" * 60)

    for object_id in range(start_id, end_id + 1):
        # Construct the specific target URL
        target_url = f"{BASE_URL}{object_id}"

        try:
            # Send the HTTP request
            response = requests.get(target_url, headers=HEADERS, timeout=5)

            # Check for indicators of an IDOR vulnerability
            if response.status_code == 200:
                print(f"[+] Potential IDOR Found! ID: {object_id} | Status: 200 OK")
            elif response.status_code == 403 or response.status_code == 401:
                print(f"[-] Secure: ID {object_id} returned {response.status_code}")
            else:
                print(f"[.] ID {object_id} returned status code: {response.status_code}")

        except requests.exceptions.RequestException as e:
            print(f"[!] Error scanning ID {object_id}: {e}")

if __name__ == "__main__":
    # Scan user IDs from 1 to 10
    scan_idor(start_id=1, end_id=10)
    
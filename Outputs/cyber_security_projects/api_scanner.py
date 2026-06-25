import requests
import sys

# 1. Target API endpoint to test
# We use a public mock API platform that safely returns fake data for testing
 

# 2. List of common payloads used to test if an API endpoint breaks or leaks database errors
TEST_PAYLOADS = [
    "' OR '1'='1",
    "';--",
    '" OR ""="',
    "1' ORDER BY 1--",
    "admin' --"
]
TARGET_API = "https://jsonplaceholder.typicode.com/posts/1"

def scan_api_endpoint():
    print("-" * 60)
    print(f"[*] Initializing Security API Vulnerability Scan")
    print(f"[*] Target Endpoint: {TARGET_API}")
    print("-" * 60)

    # Test the baseline first to see how a normal request behaves
    try:
        baseline_response = requests.get(TARGET_API, timeout=5)
        print(f"[.] Normal API Request Status Code: {baseline_response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"[!] Critical Error: Unable to connect to target API. {e}")
        sys.exit()

    print("\n[*] Fuzzing parameters for input validation flaws...")
    print("-" * 60)

    # Loop through payloads and inject them as a query parameter (e.g., trying to exploit search/id parameters)
    for payload in TEST_PAYLOADS:
        # We test by passing the payload into a common query parameter like '?id='
        test_params = {"id": payload}
        
        try:
            response = requests.get(TARGET_API, params=test_params, timeout=5)
            
            # Look for indicators of server-side database misconfigurations or failures
            if response.status_code == 500:
                print(f"[+] Potential Flaw Found! Payload: {payload:<15} | Status: 500 Internal Server Error")
            elif "sql" in response.text.lower() or "syntax error" in response.text.lower():
                print(f"[+] Warning: Database error leaked in response! Payload: {payload}")
            else:
                print(f"[-] Secure: Payload '{payload}' handled safely (Status: {response.status_code})")
                
        except requests.exceptions.RequestException as e:
            print(f"[!] Error sending payload '{payload}': {e}")

    print("-" * 60)
    print("[*] API security scan operation completed.")
    print("-" * 60)

if __name__ == "__main__":
    scan_api_endpoint()



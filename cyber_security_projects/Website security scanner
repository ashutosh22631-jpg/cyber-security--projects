import requests
from bs4 import BeautifulSoup
import urllib.parse

class WebSecurityScanner:
    def __init__(self, target_url):
        self.target_url = target_url.rstrip('/')
        self.session = requests.Session()
        # Common payloads for testing
        self.xss_payload = "<script>alert('XSS')</script>"
        self.sqli_payload = "'"

    def check_security_headers(self):
        """Checks for missing security hardening headers."""
        print("\n[+] Checking Security Headers...")
        try:
            response = self.session.get(self.target_url, timeout=5)
            headers = response.headers
            
            important_headers = [
                "X-Frame-Options", 
                "X-Content-Type-Options", 
                "Strict-Transport-Security", 
                "Content-Security-Policy"
            ]
            
            for header in important_headers:
                if header in headers:
                    print(f"  [✓] {header}: Present ({headers[header][:30]}...)")
                else:
                    print(f"  [𝘟] {header}: MISSING")
        except requests.exceptions.RequestException as e:
            print(f"  [-] Error connecting to target: {e}")

    def get_all_forms(self, url):
        """Extracts HTML forms from the page to scan for input vulnerabilities."""
        try:
            response = self.session.get(url, timeout=5)
            soup = BeautifulSoup(response.content, "html.parser")
            return soup.find_all("form")
        except Exception:
            return []

    def scan_xss_in_forms(self):
        """Scans forms on the homepage for potential XSS vulnerabilities."""
        print("\n[+] Scanning for XSS Vulnerabilities in Forms...")
        forms = self.get_all_forms(self.target_url)
        if not forms:
            print("  [-] No forms found to test.")
            return

        print(f"  [*] Found {len(forms)} form(s). Injecting payloads...")
        for i, form in enumerate(forms):
            action = form.attrs.get("action", "")
            post_url = urllib.parse.urljoin(self.target_url, action)
            method = form.attrs.get("method", "get").lower()
            
            inputs = form.find_all("input")
            data = {}
            for input_tag in inputs:
                name = input_tag.attrs.get("name")
                type_ = input_tag.attrs.get("type", "text")
                if type_ in ["text", "search", "url", "email"]:
                    data[name] = self.xss_payload
                elif name:
                    data[name] = "test"

            try:
                if method == "post":
                    res = self.session.post(post_url, data=data, timeout=5)
                else:
                    res = self.session.get(post_url, params=data, timeout=5)

                if self.xss_payload in res.text:
                    print(f"  [🔥] VULNERABILITY FOUND: XSS detected in form #{i+1} at {post_url}")
                else:
                    print(f"  [✓] Form #{i+1}: Appears secure against basic XSS.")
            except Exception as e:
                print(f"  [-] Error testing form #{i+1}: {e}")

    def run_all(self):
        print("========================================")
        print(f" Starting Scan for: {self.target_url}")
        print("========================================")
        self.check_security_headers()
        self.scan_xss_in_forms()
        print("\n[+] Scan Complete.")

if __name__ == "__main__":
    # Get user input for target URL
    url_input = input("Enter target URL (e.g., https://example.com): ").strip()
    if not url_input.startswith("http://") and not url_input.startswith("https://"):
        url_input = "https://" + url_input

    scanner = WebSecurityScanner(url_input)
    scanner.run_all()
    
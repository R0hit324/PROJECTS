# Web Vulnerability Scanner v1.0
**Author:** R0hit324

A Python-based web vulnerability scanner that detects common security flaws in web applications.

## Features
- SQL Injection (SQLi)
- Cross-Site Scripting (XSS)
- Open Redirect
- Directory Traversal

## Output
- Live colored terminal output
- Auto-generated `.txt` report file

## Installation
```bash
pip install -r requirements.txt
```

## Usage
```bash
# Interactive mode
python scanner.py

# Direct mode
python scanner.py http://testphp.vulnweb.com
```

## Legal Disclaimer
Only use on systems you own or have explicit permission to test.
Unauthorized use is illegal.

## Test Target (legal)
- http://testphp.vulnweb.com  ← intentionally vulnerable site by Acunetix

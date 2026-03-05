# AIZEN - Advanced Recon Framework

AIZEN is a **multi-module passive reconnaissance and intelligence gathering framework** built for **ethical hackers, bug bounty hunters, and security researchers**.

The tool gathers **domain infrastructure intelligence, security configuration, and OSINT data** from publicly available sources and presents it in:

• Clean terminal output
• JSON report
• HTML security dashboard

---

# Features

AIZEN performs several reconnaissance tasks automatically.

### Infrastructure Discovery

* Resolve domain IP addresses
* Identify hosting infrastructure

### Subdomain Enumeration

* Discover subdomains from certificate transparency logs
* Expands attack surface visibility

### Server Location Intelligence

* Detect hosting country, region, city
* Identify ISP

### WHOIS Lookup

* Domain registrar
* Domain age detection

### DNS Enumeration

* A Records
* MX Records
* NS Records
* TXT Records

### SSL/TLS Analysis

* Detect certificate validity
* Identify expiration date

### Security Header Analysis

Detects missing security headers:

* HSTS
* Content Security Policy

### Email OSINT Discovery

Extracts public email addresses from the website.

### Technology Fingerprinting

Detects technologies used by the website:

* Web servers
* Programming languages
* Frameworks
* Analytics tools

### Directory Discovery

Find hidden directories like:

* `/admin`
* `/login`
* `/dashboard`

### Open Port Scanning

Detects common open ports:

* 21 FTP
* 22 SSH
* 80 HTTP
* 443 HTTPS
* 8080 HTTP-ALT

### JavaScript Endpoint Extraction

Extract hidden API endpoints from JavaScript files.

### Wayback Machine Analysis

Fetches **older versions of the website**.

### Archived URL Discovery

Finds hidden endpoints from archived data.

### Report Generation

Automatically generates:

* JSON scan report
* HTML dashboard report

Reports are saved in:

```text
reports/
```

---

# Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/aizen-recon.git
cd aizen-recon
```

Install dependencies:

```bash
pip install requests python-whois dnspython builtwith beautifulsoup4
```

---

# Usage

Run the scanner:

```bash
python aizen.py --domain example.com
```

Example:

```bash
python aizen.py --domain crawlhyderabad.in
```

---

# Example Output

```text
 █████╗ ██╗███████╗███████╗███╗   ██╗
██╔══██╗██║╚══███╔╝██╔════╝████╗  ██║
███████║██║  ███╔╝ █████╗  ██╔██╗ ██║
██╔══██║██║ ███╔╝  ██╔══╝  ██║╚██╗██║
██║  ██║██║███████╗███████╗██║ ╚████║
╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═══╝

AIZEN Advanced Recon Framework

+==========================================================+
| Target: crawlhyderabad.in                                |
+==========================================================+

+==========================================================+
| INFRASTRUCTURE                                           |
+==========================================================+

IP Address : 72.61.230.175


+==========================================================+
| SERVER LOCATION                                          |
+==========================================================+

Country : India
Region  : Maharashtra
City    : Mumbai
ISP     : Sprint Communications


+==========================================================+
| SUBDOMAINS                                               |
+==========================================================+

crawlhyderabad.in
www.crawlhyderabad.in
*.crawlhyderabad.in


+==========================================================+
| DNS                                                      |
+==========================================================+

A   : 72.61.230.175
MX  : smtp.google.com
NS  : jamie.ns.cloudflare.com
TXT : v=spf1 include:_spf.google.com ~all


+==========================================================+
| TECHNOLOGY                                               |
+==========================================================+

Web Server           : nginx
Programming Language : PHP
Analytics            : Google Analytics


+==========================================================+
| DIRECTORY BRUTE FORCE                                    |
+==========================================================+

https://crawlhyderabad.in/admin
https://crawlhyderabad.in/login
https://crawlhyderabad.in/dashboard


+==========================================================+
| OPEN PORTS                                               |
+==========================================================+

22
80
443


+==========================================================+
| OLDER WEBSITE VERSIONS                                   |
+==========================================================+

2024-02-18 -> https://web.archive.org/web/20240218102233/crawlhyderabad.in
2024-01-14 -> https://web.archive.org/web/20240114091245/crawlhyderabad.in


+==========================================================+
| ARCHIVED URLS                                            |
+==========================================================+

/admin
/login
/api/users
/dashboard
```

---

# Reports

After each scan, AIZEN generates reports automatically.

### JSON Report

```text
reports/scan_timestamp.json
```

### HTML Dashboard

```text
reports/scan_timestamp.html
```

The HTML dashboard displays the scan results in a **clean security report format**.

---



# Disclaimer

This tool is intended **only for educational purposes and authorized security testing**.

Do not scan systems without permission.

Unauthorized scanning may violate laws and regulations.

---

# Author

Khaleel Basha

Ethical Hacking & Security Research Projects

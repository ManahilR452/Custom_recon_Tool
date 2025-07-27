# Custom Reconnaissance Tool

A professional, modular CLI-based reconnaissance tool for both passive and active information gathering, designed for penetration testing and red teaming exercises.

---

## 🔍 Features

### Passive Reconnaissance
- **WHOIS Lookup:** Retrieves domain registration information.
- **DNS Enumeration:** Collects A, MX, TXT, and NS records.
- **Subdomain Enumeration:** Leverages crt.sh and other sources to discover subdomains.

### Active Reconnaissance
- **Port Scanning:**
  - Scan **common ports** or a **custom port range** specified by the user.
  - Provides estimated scan time before proceeding.
- **Banner Grabbing:** Attempts to identify services running on open ports.
- **Technology Detection:** Inspects HTTP headers to detect technologies in use.

### Reporting
- Generates structured reports in **TXT** and **JSON** formats.
- Includes **timestamps, target details**, and complete findings.
- **Logs:** Detailed logs with verbosity levels and colored outputs for better visibility.

---

## 🚀 Usage

### Install Dependencies

pip install -r requirements.txt

### Example Usage:
python main.py example.com --whois --dns --subdomains --portscan --banner --tech --report
Command-Line Flags:
- --whois → Perform WHOIS lookup
- --dns → Perform DNS enumeration
- --subdomains → Find subdomains
- --portscan → Scan open ports
- --banner → Grab service banners
- --tech → Detect server technologies
- --report → Generate reports (TXT + JSON)

### Disclaimer
This tool is developed strictly for educational and research purposes only.
Unauthorized scanning or reconnaissance on systems you do not own or have explicit permission to test is illegal and unethical.
Always ensure you have proper authorization before running any security assessments.

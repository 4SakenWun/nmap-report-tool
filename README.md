# Nmap Vulnerability Scanner & Report Generator
A Python-based penetration testing tool that automates nmap vulnerability scanning and generates professional reports in PDF, DOCX, text, HTML, Markdown, or JSON.

Roadmap: See the planned enhancements and future CEH-friendly projects in [ROADMAP.md](./ROADMAP.md).

---
## ⚠️ LEGAL DISCLAIMER & WARNING ⚠️

**READ THIS ENTIRE SECTION BEFORE USING THIS TOOL**
## Versioning and Releases

- Standard: Semantic Versioning (SemVer) — MAJOR.MINOR.PATCH
   - MAJOR: incompatible changes
   - MINOR: backwards‑compatible features
   - PATCH: backwards‑compatible fixes

- Single source of truth: `app_version.py` (`__version__`)
   - Update this value on every release
   - Use `python main.py --version` to verify

- Changelog: `CHANGELOG.md` using Keep a Changelog format

### How to cut a new release

1) Update version and changelog
```powershell
# Edit version
code .\app_version.py   # set __version__ = "1.x.y"

# Update CHANGELOG.md with new section and date
```

2) Commit and tag
```powershell
git add app_version.py CHANGELOG.md README.md
git commit -m "chore(release): 1.x.y"

git tag -a v1.x.y -m "Release 1.x.y"

git push; git push origin v1.x.y
```

3) Create GitHub Release
- Open the repo → Releases → "Draft a new release"
- Choose tag `v1.x.y`
- Title: `1.x.y`
- Click "Generate release notes" or paste from CHANGELOG
- Publish

4) Post‑release checklist
- Verify `python main.py --version` prints the new version
- Ensure README/QUICK_START examples still work

Tip: For pre‑releases, tag as `v1.1.0-rc.1` and mark the release as a pre‑release on GitHub.

### Auto GitHub Release (enabled)

When a tag matching `v*` is pushed (e.g., `v1.2.0`), a GitHub Action automatically creates a Release with generated notes.

No extra steps required beyond running the bump script (which pushes the tag):

```powershell
# Typical flow (auto-detect bump from commits)
pwsh ./scripts/bump-release.ps1 -Auto

# Or explicit bump
pwsh ./scripts/bump-release.ps1 -Bump minor
```

This workflow lives at `.github/workflows/release.yml`.

### Using the bump-release script (Windows PowerShell)

The repo includes `scripts/bump-release.ps1` to automate version bumps, changelog, tagging, and pushing.

Examples:

```powershell
# Patch bump (default) — reads commits since last tag for changelog
pwsh ./scripts/bump-release.ps1

# Explicit minor bump
pwsh ./scripts/bump-release.ps1 -Bump minor

# Explicit major bump
pwsh ./scripts/bump-release.ps1 -Bump major

# Auto mode (derives bump from commits: feat -> minor, breaking -> major)
pwsh ./scripts/bump-release.ps1 -Auto

# Pre-release (e.g., 1.2.0-rc.1)
pwsh ./scripts/bump-release.ps1 -Bump minor -Pre rc.1

# Do everything but skip pushing (for dry run)
pwsh ./scripts/bump-release.ps1 -NoPush
```

What it does:
- Updates `app_version.py` (__version__)
- Updates the Version line in `README.md`
- Prepends a new section to `CHANGELOG.md` using commits since the last tag
- Creates an annotated tag and pushes (unless `-NoPush`)

### Legal Notice

This software is provided for **EDUCATIONAL AND AUTHORIZED SECURITY TESTING PURPOSES ONLY**. By downloading, installing, or using this tool, you acknowledge and agree to the following terms:

1. **Authorization Requirement**: You must obtain **explicit written permission** from the owner of any system, network, or infrastructure before conducting any scans or security assessments.

2. **Legal Compliance**: Unauthorized access to computer systems, networks, or data is **ILLEGAL** under laws including but not limited to:
   - Computer Fraud and Abuse Act (CFAA) - United States (18 U.S.C. § 1030)
   - Computer Misuse Act 1990 - United Kingdom
   - EU Directive 2013/40/EU on attacks against information systems
   - Similar legislation in other jurisdictions worldwide

3. **Liability Disclaimer**: 
   - The author(s) and contributor(s) of this software accept **NO LIABILITY** for any misuse, damage, or illegal activity conducted with this tool
   - You assume **FULL RESPONSIBILITY** for your actions and any consequences thereof
   - The author(s) are **NOT RESPONSIBLE** for any criminal charges, civil lawsuits, or other legal actions resulting from your use of this software

4. **No Warranty**: This software is provided "AS IS" without warranty of any kind, express or implied

5. **Intended Use**: This tool is designed exclusively for:
   - Authorized penetration testing engagements with written contracts
   - Security assessments on systems you own or manage
   - Educational purposes in controlled lab environments
   - Authorized bug bounty programs
   - Legal Capture The Flag (CTF) competitions and training platforms

### Criminal Penalties Warning

Unauthorized use of this tool may result in:
- **Criminal prosecution** with potential imprisonment
- **Significant financial penalties and fines**
- **Civil lawsuits** for damages
- **Permanent criminal record**
- **Loss of professional certifications**
- **Termination of employment**

### Your Responsibility

By using this software, you certify that:
- [ ] You have read and understood this disclaimer in its entirety
- [ ] You will only use this tool on systems for which you have explicit written authorization
- [ ] You understand the legal consequences of unauthorized computer access
- [ ] You accept full responsibility for all activities conducted with this tool
- [ ] You will comply with all applicable local, state, national, and international laws

**IF YOU DO NOT AGREE TO THESE TERMS, DO NOT USE THIS SOFTWARE.**

---

## Features

- **Multiple Scan Types**: Basic, vulnerability-focused, and aggressive scanning modes
- **Professional Reports**: Generate reports in PDF, DOCX, text, HTML, Markdown, or JSON
- **Cross-Platform**: Works on Linux (Kali, Ubuntu), macOS, and Windows
- **Easy to Use**: Simple command-line interface
- **Modular Design**: Easy to extend with additional features
- **Detailed Output**: Service detection, version identification, and vulnerability findings
- **Severity-Aware**: Severity per port/finding, summaries, and color-coding in HTML/PDF

## Prerequisites

### Required Software

1. **Python 3.7+**
   - Check version: `python --version` or `python3 --version`

2. **Nmap**
   - **Linux (Debian/Ubuntu/Kali)**:
     ```bash
     sudo apt-get update
     sudo apt-get install nmap
     ```
   - **macOS**:
     ```bash
     brew install nmap
     ```
   - **Windows**:
     - Download from [nmap.org](https://nmap.org/download.html)
     - Add nmap to your system PATH

## Installation

### Step 1: Verify Prerequisites

Before installing, ensure you have:
- Python 3.7 or higher installed
- Nmap installed and accessible from command line
- pip (Python package manager) installed

**Check your Python version**:
```bash
python --version
# or on some systems:
python3 --version
```

**Check if nmap is installed**:
```bash
nmap --version
```

If nmap is not installed, see the **Installing Nmap** section below.

### Step 2: Download the Project

**Option A - Clone with Git** (recommended if you have git):
```bash
cd ~/Documents  # or your preferred directory
git clone <your-repository-url>
cd nmap_scanner_reports
```

**Option B - Manual Download**:
1. Download the project as a ZIP file
2. Extract to your Documents folder (or preferred location)
3. Open terminal/command prompt and navigate to the folder:
   ```bash
   cd ~/Documents/nmap_scanner_reports  # Linux/macOS
   # or
   cd C:\Users\YourUsername\Documents\nmap_scanner_reports  # Windows
   ```

### Step 3: Set Up Python Virtual Environment (Recommended)

Using a virtual environment keeps your project dependencies isolated:

**On Linux/macOS**:
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

**On Windows**:
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate
```

You'll see `(venv)` appear in your terminal prompt when activated.

### Step 4: Install Python Dependencies

With your virtual environment activated:

```bash
pip install -r requirements.txt
```

This installs:
- `reportlab` - for PDF report generation
- `python-docx` - for DOCX report generation

**Verify installation**:
```bash
pip list
```

You should see `reportlab` and `python-docx` in the list.

### Step 5: Install Nmap

If you don't have nmap installed:

**Linux (Debian/Ubuntu/Kali)**:
```bash
sudo apt-get update
sudo apt-get install nmap
```

**Linux (Red Hat/CentOS/Fedora)**:
```bash
sudo yum install nmap
# or
sudo dnf install nmap
```

**macOS**:
```bash
# Using Homebrew (install Homebrew first from brew.sh if needed)
brew install nmap
```

**Windows**:
1. Download the installer from [https://nmap.org/download.html](https://nmap.org/download.html)
2. Run the installer (choose the default options)
3. **IMPORTANT**: During installation, check "Add Nmap to PATH"
4. Restart your terminal/command prompt after installation
5. Verify installation: `nmap --version`

### Step 6: Verify Installation

Test that everything is working:

```bash
# Test the scanner (replace with authorized target)
python main.py -t scanme.nmap.org -o test_report.txt -v
```

If successful, you'll see scan output and `test_report.txt` will be created.

### Understanding the Authorization Check

By default, this tool will display a legal warning banner and prompt you to confirm you have written authorization before scanning. This is a safety feature to prevent accidental unauthorized scanning.

**Example of what you'll see**:
```
================================================================================
               Nmap Vulnerability Scanner & Report Generator
                    For Authorized Use Only - CEH Edition
================================================================================

WARNING: Ensure you have explicit written authorization before scanning any target.
         Unauthorized scanning may be illegal in your jurisdiction.

AUTHORIZATION CHECK
--------------------------------------------------------------------------------
Do you have WRITTEN AUTHORIZATION to scan this target? (yes/no):
```

**When to use `--skip-auth-check`**:
- TryHackMe, HackTheBox, or similar authorized training platforms
- Your own home lab / virtual machines
- Docker containers you're running locally
- Systems you own and are testing

**When NOT to use `--skip-auth-check`**:
- Client penetration testing engagements (you still need authorization, but the prompt reminds you)
- Production systems (even if you have permission, the prompt serves as a reminder)
- Any system you don't own or haven't confirmed authorization for

---

## Detailed Usage Guide

### Understanding Command-Line Arguments

The scanner uses the following syntax:

```bash
python main.py -t <target> [options] -o <output_file>
```

### Required Arguments

| Argument | Description | Example |
|----------|-------------|---------|
| `-t, --target` | Target IP address or hostname | `-t 192.168.1.1` or `-t example.com` |
| `-o, --output` | Output file path (use extension or `--format`) | `-o scan_report.html` |

### Optional Arguments

| Argument | Description | Options | Default |
|----------|-------------|---------|---------|
| `-s, --scan-type` | Type of scan to perform | `basic`, `vuln`, `aggressive` | `basic` |
| `-p, --ports` | Specific ports to scan | Port ranges or comma-separated | All common ports |
| `-v, --verbose` | Show detailed output during scan | Flag (no value needed) | Disabled |
| `--skip-auth-check` | Skip authorization prompt | Flag (use ONLY for authorized labs) | Disabled |
| `--format` | Explicit output format (overrides extension) | `pdf, docx, txt, html, md, json, csv` | Inferred from `-o` |
| `--min-severity` | Minimum severity to include | `info, low, medium, high, critical` | none |
| `--exclude-ports` | Comma-separated ports to exclude | e.g., `22,3389` | none |
| `--exclude-services` | Comma-separated services to exclude | e.g., `ssh,rdp` | none |
| `--only-uncommon-ports` | Exclude common well-known ports | Flag | Disabled |

**IMPORTANT**: By default, the scanner will prompt you to confirm you have written authorization. This is a safety measure to prevent accidental unauthorized scanning. Use `--skip-auth-check` ONLY when working in authorized lab environments like TryHackMe, HackTheBox, or your own test systems.

### Scan Types Explained

**1. Basic Scan (`-s basic`)**
- Service version detection
- Default nmap scripts
- Best for: Quick assessments, identifying running services
- Speed: Fast (1-5 minutes typically)
- Example: `python main.py -t 192.168.1.1 -s basic -o basic_scan.pdf`

**2. Vulnerability Scan (`-s vuln`)**
- Runs nmap vulnerability detection scripts
- Checks for known CVEs
- Best for: Finding potential security issues
- Speed: Moderate (5-15 minutes)
- Example: `python main.py -t 192.168.1.1 -s vuln -o vuln_scan.pdf`

**3. Aggressive Scan (`-s aggressive`)**
- OS detection
- Version detection
- Script scanning
- Traceroute
- Best for: Comprehensive assessment
- Speed: Slow (10-30 minutes)
- ⚠️ **WARNING**: More likely to be detected by IDS/IPS
- Example: `python main.py -t 192.168.1.1 -s aggressive -o full_scan.pdf`

### Port Specification

You can limit scans to specific ports for faster results:

```bash
# Scan common web ports
python main.py -t example.com -p 80,443,8080,8443 -o web_scan.pdf

# Scan a range of ports
python main.py -t 10.0.0.1 -p 1-1000 -o first_1000_ports.pdf

# Scan specific ports and ranges combined
python main.py -t 192.168.1.1 -p 22,80,443,3000-4000 -o custom_scan.pdf
```

### Filtering and Prioritization

Filter results before rendering the report:

```bash
# Only include Medium+ and drop SSH/RDP
python main.py -t 10.0.0.5 -s vuln -o filtered.md --min-severity medium --exclude-services ssh,rdp

# Exclude specific ports and show only uncommon ones
python main.py -t 10.0.0.5 -o filtered.html --exclude-ports 22,3389 --only-uncommon-ports

# Force JSON format regardless of extension
python main.py -t 10.0.0.5 --format json -o scan
```

Note: Only open ports are reported by design; `--only-open` is not needed.

### Output Format Selection

Choose your report format based on your needs. You can set it by file extension in `-o` or explicitly with `--format` (`pdf|docx|txt|html|md|json|csv`). If both are provided, `--format` wins.

**PDF Reports** (`.pdf`)
- Professional, polished appearance
- Cannot be easily modified
- Best for: Client deliverables, final reports
- Example: `python main.py -t target.com -o final_report.pdf`

**DOCX Reports** (`.docx`)
- Microsoft Word format
- Easy to edit and customize
- Best for: Draft reports, collaborative editing
- Example: `python main.py -t target.com -o draft_report.docx`

**Text Reports** (`.txt`)
- Plain text format
- Lightweight and fast
- Best for: Quick reference, command-line viewing
- Example: `python main.py -t target.com -o quick_scan.txt`

**HTML Reports** (`.html`)
- Styled tables with color-coded severities and summaries
- Best for: Quick sharing or viewing in a browser
- Example: `python main.py -t target.com -o report.html`

**Markdown Reports** (`.md`)
- Portable tables with severity column
- Best for: Wikis, code reviews, and versioning
- Example: `python main.py -t target.com -o report.md`

**JSON Exports** (`.json`)
- Canonical structured output for automation
- Best for: Pipelines and integrations
- Example: `python main.py -t target.com -o out.json` or `--format json`

## Practical Examples

### Example 1: Basic Website Assessment

**Scenario**: You want to quickly check what services are running on a web server you manage.

```bash
python main.py -t www.yourcompany.com -s basic -p 80,443 -o website_check.pdf -v
```

**What this does**:
- Scans ports 80 (HTTP) and 443 (HTTPS)
- Identifies web server software and versions
- Generates a PDF report
- Shows verbose output

---

### Example 2: Vulnerability Assessment for Penetration Test

**Scenario**: You have a signed contract to perform a pentest on a client's server.

```bash
python main.py -t 10.50.1.100 -s vuln -o client_vulnscan_2024-11-13.docx -v
```

**What this does**:
- Runs comprehensive vulnerability scripts
- Checks for known CVEs and security issues
- Creates a DOCX report (easy to edit before final delivery)
- Includes date in filename for record-keeping

---

### Example 3: Internal Network Audit

**Scenario**: Your IT department authorized you to scan the corporate mail server.

```bash
python main.py -t mailserver.internal.company.com -s basic -p 25,587,993,995 -o mail_server_audit.pdf
```

**What this does**:
- Scans common mail ports (SMTP, SMTPS, IMAPS, POP3S)
- Quick service identification
- Professional PDF for IT management

---

### Example 4: Quick Text Report for Documentation

**Scenario**: You need to document which ports are open for your system documentation.

```bash
python main.py -t 192.168.1.50 -p 1-1000 -o port_inventory.txt
```

**What this does**:
- Scans first 1000 ports
- Creates simple text file
- Easy to include in technical documentation

---

## Using with Legal Training Platforms

### TryHackMe.com

[TryHackMe](https://tryhackme.com) is a legal, authorized platform for practicing penetration testing skills.

**Step-by-Step Guide**:

1. **Sign up for TryHackMe**:
   - Go to [https://tryhackme.com](https://tryhackme.com)
   - Create a free account
   - Read and accept their terms of service

2. **Start a Room**:
   - Navigate to "Rooms" or "Learning Paths"
   - Choose a beginner room (e.g., "Basic Pentesting", "Simple CTF")
   - Click "Join Room"

3. **Connect to OpenVPN**:
   - Download your TryHackMe OpenVPN configuration file
   - Connect using: `sudo openvpn your_config_file.ovpn`
   - Verify connection: `ifconfig` (look for `tun0` interface)

4. **Get Your Target IP**:
   - Click "Start Machine" in the room
   - Wait for the machine to deploy (shows IP like `10.10.x.x`)

5. **Scan the Target**:
   ```bash
   # Basic scan (use --skip-auth-check for lab environments to avoid the prompt)
   python main.py -t 10.10.x.x -s basic -o thm_initial_scan.txt -v --skip-auth-check
   
   # Vulnerability scan
   python main.py -t 10.10.x.x -s vuln -o thm_vuln_scan.pdf --skip-auth-check
   
   # Scan specific ports found in initial scan
   python main.py -t 10.10.x.x -p 80,22,445 -o thm_detailed.docx --skip-auth-check
   ```

6. **Use the Reports**:
   - Open the generated report
   - Identify services and versions
   - Look for vulnerabilities
   - Use this information to complete the room challenges

**TryHackMe Example Workflow**:
```bash
# 1. Initial scan to discover services
python main.py -t 10.10.50.100 -s basic -o thm_discovery.txt -v --skip-auth-check

# 2. Review the text report to see what's running

# 3. Deep vulnerability scan on discovered ports
python main.py -t 10.10.50.100 -s vuln -p 80,22,445 -o thm_vulnerabilities.pdf --skip-auth-check

# 4. Document your findings
# The PDF report serves as your penetration testing notes
```

### HackTheBox.com

[HackTheBox](https://www.hackthebox.com) is another legal platform for security training.

**Usage with HTB**:

1. **Sign up and connect to HTB VPN**:
   - Create account at [https://www.hackthebox.com](https://www.hackthebox.com)
   - Download VPN configuration
   - Connect: `sudo openvpn lab_yourusername.ovpn`

2. **Spawn a machine**:
   - Choose a machine from the "Machines" list
   - Click "Join Machine" or "Spawn Machine"
   - Note the target IP (e.g., `10.129.x.x`)

3. **Scan and document**:
   ```bash
   # Initial enumeration
   python main.py -t 10.129.x.x -s basic -o htb_enum.txt -v --skip-auth-check
   
   # Detailed vulnerability assessment
   python main.py -t 10.129.x.x -s vuln -o htb_vulns.pdf --skip-auth-check
   ```

### PortSwigger Web Security Academy

For web application testing practice:

1. Visit [https://portswigger.net/web-security](https://portswigger.net/web-security)
2. Use the tool to scan lab environments (authorized by PortSwigger)
3. Example:
   ```bash
   python main.py -t <lab-id>.web-security-academy.net -p 443 -o portswigger_lab.txt
   ```

### Your Own Lab Environment

**Highly Recommended**: Set up your own practice lab:

1. **Using VirtualBox/VMware**:
   - Download vulnerable VMs:
     - Metasploitable 2/3
     - DVWA (Damn Vulnerable Web App)
     - OWASP Broken Web Applications
   - Import into VirtualBox/VMware
   - Configure host-only network
   
2. **Scan Your Lab**:
   ```bash
   # Scan your vulnerable VM (skip auth check for your own lab)
   python main.py -t 192.168.56.101 -s vuln -o lab_practice.pdf -v --skip-auth-check
   ```

**Docker Lab Setup**:
```bash
# Run DVWA in Docker
docker run -d -p 80:80 vulnerables/web-dvwa

# Scan it (skip auth check for localhost lab)
python main.py -t localhost -p 80 -o dvwa_scan.txt --skip-auth-check
```

---

## Common Use Cases

### Basic Command Structure

```bash
python main.py -t <target> -o <output_file>
```

### Command-Line Options

- `-t, --target`: **Required** - Target IP address or hostname to scan
- `-o, --output`: **Required** - Output file path (must end in .pdf, .docx, or .txt)
- `-s, --scan-type`: Scan type - `basic`, `vuln`, or `aggressive` (default: basic)
- `-p, --ports`: Port specification (e.g., `1-1000` or `80,443,8080`)
- `-v, --verbose`: Enable verbose output during scanning

### Examples

---

## Additional Usage Examples

**Basic scan with PDF report**:
```bash
python main.py -t 192.168.1.1 -o report.pdf
```

**Vulnerability scan with DOCX report**:
```bash
python main.py -t scanme.nmap.org -s vuln -o vulnerability_report.docx
```

**Aggressive scan on specific ports**:
```bash
python main.py -t 10.0.0.1 -s aggressive -p 80,443,8080 -o detailed_scan.pdf
```

**Scan with verbose output**:
```bash
python main.py -t example.com -s basic -o results.txt -v
```

---

## Best Practices for Penetration Testing

### Before Scanning

1. **Get Written Authorization**:
   - Obtain a signed contract or letter of authorization
   - Define scope (which systems/networks are authorized)
   - Specify testing timeframe
   - Keep authorization documents with your reports

2. **Understand the Scope**:
   - Know what is in-scope and out-of-scope
   - Verify IP addresses and hostnames
   - Understand any restrictions (time windows, scan types, etc.)

3. **Prepare Your Environment**:
   ```bash
   # Create a project folder for the engagement
   mkdir ~/pentests/client_name_2024-11-13
   cd ~/pentests/client_name_2024-11-13
   
   # Keep authorization documents here
   # Run scans from this directory
   # All reports will be organized in one place
   ```

### During Scanning

1. **Start with Less Intrusive Scans**:
   ```bash
   # First: Basic scan to understand the target
   python main.py -t target.com -s basic -o 01_initial_scan.txt -v
   
   # Then: More detailed vulnerability scan
   python main.py -t target.com -s vuln -o 02_vuln_scan.pdf
   ```

2. **Document Everything**:
   - Use descriptive filenames with dates
   - Enable verbose mode (`-v`) to see what's happening
   - Keep notes about unusual findings

3. **Be Professional**:
   - Don't scan outside business hours unless authorized
   - Watch for signs you're causing issues (system slowdown)
   - Have client contact information ready

### After Scanning

1. **Secure Your Reports**:
   ```bash
   # Reports contain sensitive information
   # Set appropriate permissions (Linux/macOS)
   chmod 600 *.pdf *.docx
   ```

2. **Review Before Delivery**:
   - Verify all findings
   - Remove false positives
   - Add context and recommendations

3. **Archive Your Work**:
   - Keep copies of all scans and reports
   - Maintain chain of custody
   - Follow data retention policies

---

## Workflow Example: Complete Penetration Test

This is a complete workflow showing how to use this tool in a real engagement:

```bash
# Step 1: Create project directory
mkdir ~/pentests/acme_corp_nov2024
cd ~/pentests/acme_corp_nov2024

# Step 2: Initial discovery scan
python main.py -t 10.50.1.100 -s basic -o 01_discovery.txt -v
# Review the text file to see what services are running

# Step 3: Detailed vulnerability scan on discovered services
python main.py -t 10.50.1.100 -s vuln -o 02_vulnerability_scan.docx -v
# Review DOCX, add notes, identify critical findings

# Step 4: Focused scan on specific services
python main.py -t 10.50.1.100 -p 80,443,8080 -s aggressive -o 03_web_services.pdf
# Generate final PDF for web services

# Step 5: Compile final report
# Edit 02_vulnerability_scan.docx with:
# - Executive summary
# - Methodology
# - Findings with severity ratings
# - Remediation recommendations
# - Export as final PDF

# Step 6: Clean up and secure
chmod 600 *.pdf *.docx *.txt
ls -lh  # Verify all reports are present
```

---

### Scan Types

- **basic**: Standard scan with service version detection and default scripts
- **vuln**: Focused vulnerability scanning using nmap's vuln scripts
- **aggressive**: Comprehensive scan including OS detection and traceroute

## Output Formats

### PDF Reports
- Professional formatting with tables and sections
- Includes scan summary, host details, open ports, and vulnerabilities
- Suitable for client deliverables

### DOCX Reports
- Microsoft Word format for easy editing
- Structured layout with tables
- Can be customized before final delivery

### Text Reports
- Simple plain text format
- Quick overview of scan results
- Useful for quick reference or command-line viewing

### HTML Reports
- Clean layout with inline CSS and severity badges
- Includes a severity summary table

### Markdown Reports
- Portable tables for wikis and version control
- Includes severity column and summary

### JSON Exports
- Canonical structure used internally across renderers
- Ideal for downstream automation and pipelines

## Project Structure

```
nmap_scanner_reports/
├── scanner/
│   ├── __init__.py
│   └── nmap_scanner.py      # Core scanning logic
├── reports/
│   ├── __init__.py
│   └── report_generator.py  # Report generation (PDF/DOCX/TXT)
├── main.py                  # CLI entry point
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Legal & Ethical Considerations

**IMPORTANT**: This tool is designed for authorized security assessments only.

- Only scan systems you own or have explicit written permission to test
- Unauthorized port scanning may be illegal in your jurisdiction
- Always follow responsible disclosure practices
- Comply with all applicable laws and regulations
- Use this tool ethically and professionally

## Future Enhancements

This project is designed to be modular and extensible. Planned features include:

For a broader, CEH-focused roadmap and additional project ideas, see [ROADMAP.md](./ROADMAP.md).

- AI-powered vulnerability analysis and recommendations
- Web-based dashboard interface
- Database storage for historical scans
- Multiple target support (network ranges)
- Custom scan profiles and templates
- Integration with vulnerability databases (CVE, NVD)
- Automated remediation suggestions

## Troubleshooting

### "nmap is not installed or not found in PATH"
- Ensure nmap is installed using the commands in the Prerequisites section
- Verify nmap is in your system PATH: `nmap --version`

### "Permission denied" errors
- On Linux/macOS, some scan types may require sudo: `sudo python main.py ...`
- Ensure you have appropriate permissions on the target network

### Import errors for reportlab or python-docx
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Try upgrading pip: `pip install --upgrade pip`

### Scan times out
- Large port ranges or comprehensive scans can take time
- Try scanning specific ports with `-p` flag
- Use basic scan type for faster results

### I received a complaint or legal notice about my scanning
**STOP IMMEDIATELY** if you receive any complaint, cease and desist, or legal notice:

1. **Stop all scanning activities immediately**
2. **Document everything**:
   - Save all authorization documents
   - Save all communications
   - Save scan logs and reports
   - Note exactly what was scanned and when
3. **Contact legal counsel** if the situation is serious
4. **Respond professionally**:
   - Apologize for any confusion
   - Provide proof of authorization if you have it
   - Explain the purpose of the scan
   - Confirm you have stopped all activities
5. **Learn from the incident**:
   - Review your authorization procedures
   - Ensure scope is clearly defined in writing
   - Maintain better communication with system owners

**Prevention is key**: Always get crystal-clear, written authorization before scanning.

### Reports contain sensitive data - how do I protect them?
```bash
# Linux/macOS - Restrict file permissions
chmod 600 *.pdf *.docx *.txt

# Encrypt sensitive reports
gpg -c sensitive_report.pdf  # Creates sensitive_report.pdf.gpg

# Securely delete original after encrypting
shred -u sensitive_report.pdf

# Windows - Use BitLocker or encrypt the folder
# Right-click folder → Properties → Advanced → Encrypt contents
```

---

## Security and Privacy

### Protecting Your Scan Data

Scan reports often contain sensitive information about security vulnerabilities. Protect them:

1. **Set restrictive permissions** (Linux/macOS):
   ```bash
   chmod 700 ~/pentests  # Only you can access
   chmod 600 *.pdf *.docx  # Only you can read/write reports
   ```

2. **Encrypt sensitive data**:
   ```bash
   # Using GPG
   gpg -c confidential_report.pdf
   
   # Using 7-Zip (Windows)
   7z a -p -mhe=on confidential_report.7z confidential_report.pdf
   ```

3. **Secure deletion** when reports are no longer needed:
   ```bash
   # Linux
   shred -vfz -n 10 old_report.pdf
   
   # macOS
   srm -vz old_report.pdf
   
   # Windows - Use secure deletion tool like Eraser
   ```

4. **Use full disk encryption**:
   - Linux: LUKS
   - macOS: FileVault
   - Windows: BitLocker

### Data Retention Policy

As a penetration tester:
- Keep reports only as long as required by contract
- Follow your organization's data retention policies
- Securely destroy old reports
- Never share client data without explicit permission

---

## Legal Resources and References

### Laws to Be Aware Of

**United States**:
- Computer Fraud and Abuse Act (CFAA) - 18 U.S.C. § 1030
- [CFAA Overview](https://www.justice.gov/jm/jm-9-48000-computer-fraud)

**United Kingdom**:
- Computer Misuse Act 1990
- [CMA Overview](https://www.legislation.gov.uk/ukpga/1990/18/contents)

**European Union**:
- Directive 2013/40/EU on attacks against information systems
- GDPR considerations for handling scan data

**Australia**:
- Cybercrime Act 2001

### Professional Standards

- **EC-Council CEH Code of Ethics**: [https://www.eccouncil.org/code-of-ethics/](https://www.eccouncil.org/code-of-ethics/)
- **SANS Pen Testing Code of Ethics**: Follow responsible disclosure principles
- **Bug Bounty Program Rules**: Always read and follow platform-specific rules

### Getting Proper Authorization

**Minimum requirements for authorization documentation**:
1. Company letterhead or official email
2. Specific systems/networks/IP ranges authorized
3. Date range for testing
4. Approved testing methods
5. Points of contact
6. Signature from authorized representative

**Template language for authorization requests**:
```
Dear [System Owner],

I am requesting written authorization to perform security testing on the 
following systems:

Systems in Scope:
- [IP addresses or hostnames]
- [Network ranges]
- [Web applications]

Testing Period: [Start Date] to [End Date]

Testing Methods:
- Network vulnerability scanning
- Port scanning
- Service enumeration
- [Other approved methods]

I understand that this testing will be conducted in accordance with all 
applicable laws and your organization's policies.

Please confirm your authorization in writing.

Regards,
[Your Name]
[Your Title/Company]
```

---

## Ethical Hacking Resources

### Recommended Training Platforms (All Legal and Authorized)

- **TryHackMe**: [https://tryhackme.com](https://tryhackme.com) - Beginner-friendly
- **HackTheBox**: [https://www.hackthebox.com](https://www.hackthebox.com) - Advanced challenges
- **PentesterLab**: [https://pentesterlab.com](https://pentesterlab.com) - Web app focus
- **PortSwigger Web Security Academy**: [https://portswigger.net/web-security](https://portswigger.net/web-security)
- **VulnHub**: [https://www.vulnhub.com](https://www.vulnhub.com) - Downloadable VMs

### Bug Bounty Platforms (Legal Vulnerability Research)

- **HackerOne**: [https://www.hackerone.com](https://www.hackerone.com)
- **Bugcrowd**: [https://www.bugcrowd.com](https://www.bugcrowd.com)
- **Synack**: [https://www.synack.com](https://www.synack.com)
- **YesWeHack**: [https://www.yeswehack.com](https://www.yeswehack.com)

Always read and follow each platform's specific rules and scope!

---

## Contributing

This is a personal project for building a professional penetration testing portfolio. Suggestions and feedback are welcome.

## Project Disclaimer

This tool was created for legitimate security professionals to use in authorized engagements. The author:

- ✅ **Supports** ethical hacking and responsible security research
- ✅ **Encourages** proper authorization and legal compliance  
- ✅ **Promotes** responsible vulnerability disclosure
- ❌ **Does NOT support** illegal hacking or unauthorized access
- ❌ **Does NOT condone** malicious use of security tools
- ❌ **Accepts NO liability** for misuse by others

## License

See [LICENSE](LICENSE) file for detailed terms and conditions.

This project is licensed under MIT License with additional terms for security testing software. By using this tool, you agree to use it only for authorized and legal purposes.

## Author

Created by a Certified Ethical Hacker (CEH) for professional penetration testing workflows.

**Contact**: For questions about proper use or to report misuse, open an issue in this repository.

---

## Final Reminders

### ✅ DO:
- Get explicit written authorization before every scan
- Use on training platforms (TryHackMe, HackTheBox, etc.)
- Test your own systems and home lab
- Follow responsible disclosure practices
- Comply with all laws and regulations
- Document everything professionally
- Protect sensitive scan data

### ❌ DO NOT:
- Scan systems without written permission
- Use this tool for illegal purposes
- Share client data without authorization
- Scan production systems during business hours (unless authorized)
- Ignore scope limitations in your authorization
- Conduct scans that could cause damage or disruption
- Assume verbal authorization is sufficient

---

**🛡️ REMEMBER: With great power comes great responsibility. Use this tool ethically and legally. 🛡️**

---

**Last Updated**: November 13, 2025  
**Version**: 1.0.0

---

*For educational and authorized security assessment purposes only.*

---

## Offline Demo (No Live Scans)

Want to test the tool without touching a real target? Use the built-in sample Nmap XML and the `--xml` flag to generate reports completely offline. This avoids any network activity and is safe for demos and training.

Lab‑safe commands (Windows PowerShell):

```powershell
# HTML report from sample XML (no network scan)
python .\main.py --xml .\samples\nmap_sample.xml -o offline_demo.html --skip-auth-check

# PDF report (ReportLab required)
python .\main.py --xml .\samples\nmap_sample.xml -o offline_demo.pdf --skip-auth-check

# Markdown report
python .\main.py --xml .\samples\nmap_sample.xml -o offline_demo.md --skip-auth-check
```

Notes:
- `--xml` parses an existing Nmap XML file (`.xml` or `.xml.gz`) and never runs a live scan.
- `-t/--target` is optional in offline mode; the tool labels the target as `offline` unless you provide `-t`.
- Keep using `--skip-auth-check` for offline demos to bypass the runtime authorization prompt.
- This is the recommended way to practice report generation and verify formatting safely.



# Quick Reference Guide - Nmap Scanner

## Quick Start

```bash
# Basic scan
python main.py -t <target> -o report.pdf

# Skip authorization prompt (labs only)
python main.py -t <target> -o report.pdf --skip-auth-check
```

## Common Commands

### Quick Scans
```bash
# Fast text report
python main.py -t 192.168.1.1 -o quick.txt --skip-auth-check

# Web server check
python main.py -t example.com -p 80,443 -o web.pdf --skip-auth-check
```

### Vulnerability Assessment
```bash
# Full vulnerability scan
python main.py -t 10.0.0.1 -s vuln -o vulns.pdf

# Aggressive deep scan
python main.py -t 10.0.0.1 -s aggressive -o deep.docx
```

### TryHackMe
```bash
# Initial recon
python main.py -t 10.10.x.x -s basic -o thm_recon.txt -v --skip-auth-check

# Detailed scan
python main.py -t 10.10.x.x -s vuln -o thm_scan.pdf --skip-auth-check
```

### HackTheBox
```bash
# HTB machine scan
python main.py -t 10.129.x.x -s basic -o htb_enum.txt -v --skip-auth-check
```

## Scan Types

| Type | Speed | Detail | Use Case |
|------|-------|--------|----------|
| `basic` | Fast | Medium | Initial discovery |
| `vuln` | Medium | High | Vulnerability hunting |
| `aggressive` | Slow | Very High | Deep assessment |

## Port Specifications

```bash
# Common web ports
-p 80,443,8080,8443

# First 1000 ports
-p 1-1000

# All ports (slow!)
-p 1-65535

# Mixed
-p 22,80,443,3000-4000
```

## Output Formats

- `.pdf` - Professional client reports
- `.docx` - Editable draft reports  
- `.txt` - Quick reference

## Flags

- `-v` - Verbose output (recommended)
- `--skip-auth-check` - Skip authorization prompt (labs only)

## File Organization

```bash
# Create project structure
mkdir ~/pentests/project_name
cd ~/pentests/project_name

# Run scans with numbered sequence
python main.py -t target -o 01_discovery.txt
python main.py -t target -s vuln -o 02_vulns.pdf
python main.py -t target -p 80,443 -o 03_web.pdf
```

## Security Checklist

- [ ] Written authorization obtained
- [ ] Scope clearly defined
- [ ] Emergency contact information ready
- [ ] Reports encrypted/protected
- [ ] Working in authorized timeframe

## Emergency

If you receive a complaint:
1. STOP all scanning immediately
2. Document what was scanned
3. Gather authorization documents
4. Contact legal counsel if serious
5. Respond professionally with proof of authorization

## Legal Training Platforms

- TryHackMe: https://tryhackme.com
- HackTheBox: https://www.hackthebox.com
- VulnHub: https://www.vulnhub.com
- PentesterLab: https://pentesterlab.com

## Getting Help

```bash
python main.py --help
```

## Remember

✅ Always get written authorization  
✅ Document everything  
✅ Protect scan data  
❌ Never scan without permission  
❌ Never share client data  

---

*For authorized use only - see LICENSE and README for full legal terms*

# Project Roadmap and Ideas (CEH Portfolio)

This roadmap captures future security tooling projects you can build and showcase. Each item includes stack, core deliverables, and why it matters. Stick to authorized, lab-safe usage and include legal safeguards in every tool.

## Quick Wins for Current Repo
- Multi-target + Diffing: CIDR/file input, store results, show what changed since last scan.
- CVE Enrichment: Map service+version to CVEs, prioritize by CVSS and CISA KEV, add remediation.
- Executive Summary: Add a one-page summary with risk heatmap to PDF/DOCX.
- JSON Export: Output machine-readable JSON alongside PDF/DOCX for later ingestion.

## Beginner/Mid
- Asset Sweeper (Network Inventory)
  - Stack: Python, nmap/masscan, SQLite
  - Build: CIDR/range scan, host fingerprints, delta diff reports (HTML/PDF)
  - Why: Shows repeatable methodology and evidence tracking

- Web Enumerator Orchestrator
  - Stack: Python, requests, wafw00f, sslyze/sslscan, whatweb
  - Build: Passive + light active checks, tech stack ID, TLS/WAF findings, consolidated report
  - Why: Professional recon workflow without going overly intrusive

- OWASP ZAP Controller + Reporter
  - Stack: Python, ZAP API, python-docx/reportlab
  - Build: Start/stop ZAP, context auth, target profiles, export CWE/CVSS with remediation
  - Why: Real-world appsec automation and controlled scanning

## Intermediate
- CVE Enricher for Nmap Results
  - Stack: Python, NVD API, CISA KEV, caching
  - Build: Fetch/normalize CVEs, de-dup, prioritize (CVSS/KEV/age/exploitability), mitigation text
  - Why: Turns raw findings into actionable risk

- Windows Local Security Audit (PowerShell)
  - Stack: PowerShell 5/7
  - Build: Password policy, RDP, services, local admins, audit policy, CIS-style checks; DOCX/PDF output
  - Why: Consulting-grade host review that hiring managers recognize

- Cloud Read-Only Audit (AWS)
  - Stack: Python, boto3
  - Build: Enumerate publics, S3 ACL issues, IAM basics (read-only), SGs, GuardDuty status; risk summary
  - Why: Demonstrates cloud security fundamentals safely

- Container/Image + Host Vulnerability Pipeline
  - Stack: Trivy/Grype, Python wrapper, GitHub Actions
  - Build: Scan images/hosts, fail CI on criticals, publish artifact reports, README badge
  - Why: DevSecOps credibility and automation

## Advanced (Lab-Only)
- AD Read-Only Enumerator
  - Stack: Python (ldap3) and/or PowerShell (AD module)
  - Build: Domain info, password policy, stale accounts, SPNs, delegation flags; CSV/HTML export
  - Why: Blue-team-friendly recon that’s highly relevant

- Honeypot + Alerting
  - Stack: Cowrie/Dionaea, Python, Slack/Discord webhooks, ELK/OpenSearch
  - Build: Run honeypot, parse events, alert pipeline, dashboard (top sources/commands)
  - Why: Signals detection mindset and IR fundamentals

- Password Hygiene Audit (Lab Data Only)
  - Stack: Python, rules-based checks, optional hashcat wrappers with synthetic hashes
  - Build: Policy checks, weak patterns, rules benchmarking; clear lab-only safeguards
  - Why: Shows risk quantification carefully and ethically

## OSINT/Process
- Recon Aggregator (Ethical OSINT)
  - Stack: Python, public/rate-limited sources, rich/HTML output
  - Build: DNS/email/TLS/meta aggregation, no intrusive actions, tidy export for scoping
  - Why: Demonstrates pre-engagement recon discipline

- Findings-to-Report Converter
  - Stack: Python, Jinja2, python-docx/reportlab
  - Build: Ingest JSON/CSV from tools → normalize severity → generate executive + technical sections
  - Why: Reporting automation is a differentiator

## Implementation Guidelines
- Legal Guardrails: Banners, `--skip-auth-check`, clear disclaimers, authorization templates.
- Reporting: PDF/DOCX with severity, evidence, remediation; include dates and scope.
- Repeatability: Config profiles, sane defaults, sample datasets, CI checks where applicable.
- Versioning: SemVer, CHANGELOG, release tags; reuse your current Actions flow.

---

Pick one and build iteratively. If you want, we can scaffold any item (folders, CLI, templates) and ship a minimal MVP with sample outputs.

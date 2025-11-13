# Authorization Letter Template

Use this template to request written authorization for penetration testing.

---

## Template 1: Formal Authorization Request

```
[Your Letterhead or Company Name]
[Your Address]
[City, State ZIP]
[Date]

[Client Name]
[Client Title]
[Company Name]
[Company Address]
[City, State ZIP]

Dear [Client Name],

Subject: Request for Authorization - Security Assessment

I am writing to request formal written authorization to conduct a security 
assessment on your organization's systems as discussed.

SCOPE OF TESTING:

Systems in Scope:
- [IP Address/Range: e.g., 192.168.1.0/24]
- [Hostname: e.g., www.example.com]
- [Web Applications: e.g., https://app.example.com]
- [Other systems as agreed]

Systems Explicitly Out of Scope:
- [Any excluded systems]
- [Third-party hosted services without separate authorization]

Testing Period:
- Start Date: [MM/DD/YYYY]
- End Date: [MM/DD/YYYY]
- Preferred Testing Hours: [e.g., After business hours, 6 PM - 6 AM]

Testing Methods to be Used:
- Network vulnerability scanning (nmap, Nessus, etc.)
- Port scanning and service enumeration
- Web application security testing
- [Other methods as agreed]

Testing Methods NOT Authorized (unless specified):
- Social engineering
- Physical security testing
- Denial of service testing
- Exploitation of vulnerabilities

Deliverables:
- Detailed security assessment report
- Executive summary
- Remediation recommendations
- [Optional: Follow-up consultation]

I understand and agree that:
1. All testing will be conducted within the agreed scope only
2. I will immediately stop testing if asked by authorized personnel
3. I will immediately report any critical vulnerabilities discovered
4. All findings will be kept confidential
5. I will comply with all applicable laws and regulations

Please confirm your authorization by signing below and returning this document.

Thank you for your cooperation.

Sincerely,

[Your Signature]
[Your Printed Name]
[Your Title]
[Your Contact Information]

---

AUTHORIZATION SIGNATURE:

I, [Client Name], [Client Title] of [Company Name], hereby authorize 
[Your Name] to conduct the security assessment as described above.

I understand the scope and methods of this assessment and confirm that I 
have the authority to grant this permission.


_________________________________          _____________
Authorized Signature                       Date

_________________________________
Printed Name and Title
```

---

## Template 2: Simple Email Authorization

For less formal engagements (still get it in writing!):

```
Subject: Security Testing Authorization - [Company Name]

Dear [Your Name],

This email serves as written authorization for you to conduct security 
testing on the following systems owned by [Company Name]:

Authorized Systems:
- [List all in-scope systems, IPs, domains]

Testing Period: [Start Date] to [End Date]

Authorized Testing Methods:
- Network vulnerability scanning
- Port scanning
- [Other approved methods]

Emergency Contact: [Name, Phone, Email]

Please proceed with the assessment as discussed. Contact me immediately 
if you discover any critical vulnerabilities.

Best regards,
[Client Name]
[Client Title]
[Company Name]
[Contact Information]
```

---

## Template 3: Bug Bounty / Scope Clarification

When you need written clarification on bug bounty scope:

```
Subject: Scope Clarification Request - [Program Name]

Dear [Program Contact],

I am participating in your bug bounty program and would like written 
clarification on the following scope items before proceeding:

1. Is [specific subdomain/system] in scope for testing?
2. Are [specific testing methods] permitted?
3. [Any other scope questions]

Could you please confirm in writing so I can proceed appropriately?

Thank you,
[Your Name]
[Your Bug Bounty Profile Link]
```

---

## What to Keep in Your Records

For every engagement, maintain:

1. **Signed authorization letter** (original)
2. **All email communications** regarding scope
3. **Statements of work / contracts**
4. **Scope change notifications** (if any)
5. **Scan logs and timestamps**
6. **All deliverables and reports**

## Digital Record Keeping

```bash
# Create engagement folder
mkdir ~/pentests/client_name_YYYY-MM-DD
cd ~/pentests/client_name_YYYY-MM-DD

# Folder structure
mkdir -p {authorization,scans,reports,notes}

# Store authorization
mv authorization_letter.pdf authorization/

# Protect the folder
chmod 700 ~/pentests/client_name_YYYY-MM-DD
```

## Red Flags - When NOT to Proceed

❌ Verbal authorization only  
❌ Authorization from someone who may not have authority  
❌ Vague or unclear scope  
❌ Pressure to "just start" without proper documentation  
❌ Third-party systems without separate authorization  
❌ Scope includes production systems during business hours without explicit approval  

## When in Doubt

**ALWAYS GET IT IN WRITING**

If a client says "just start scanning," politely respond:

> "I appreciate your trust, but for both our protection, I need written 
> authorization before beginning any security testing. This protects both 
> of us legally and ensures we have clear documentation of the scope. 
> I can provide a template if that would help."

---

## Legal Note

This template is provided for informational purposes only and does not 
constitute legal advice. Consult with an attorney to ensure your 
authorization documents meet the legal requirements in your jurisdiction.

---

**Remember**: No authorization = No testing. Period.

*Last Updated: November 13, 2024*

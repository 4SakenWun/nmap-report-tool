from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict, Any


SEVERITY_ORDER = {"info": 0, "low": 1, "medium": 2, "high": 3, "critical": 4}


@dataclass
class Address:
    type: str
    address: str


@dataclass
class Service:
    name: str = "unknown"
    product: str = ""
    version: str = ""
    extrainfo: str = ""


@dataclass
class ScriptFinding:
    id: str
    output: str
    severity: str = "info"


@dataclass
class PortEntry:
    port: int
    protocol: str
    state: str
    service: Optional[Service] = None
    scripts: List[ScriptFinding] = field(default_factory=list)
    severity: str = "info"


@dataclass
class HostEntry:
    status: str
    addresses: List[Address] = field(default_factory=list)
    hostnames: List[str] = field(default_factory=list)
    ports: List[PortEntry] = field(default_factory=list)
    os: Optional[Dict[str, str]] = None


@dataclass
class ScanResult:
    target: str
    scan_time: str
    scanner_version: str
    hosts: List[HostEntry]

    def to_dict(self) -> Dict[str, Any]:
        def _convert(obj):
            if isinstance(obj, (Address, Service, ScriptFinding, PortEntry, HostEntry)):
                return asdict(obj)
            if isinstance(obj, list):
                return [_convert(x) for x in obj]
            return obj

        return {
            "target": self.target,
            "scan_time": self.scan_time,
            "scanner_version": self.scanner_version,
            "hosts": _convert(self.hosts),
        }


COMMON_PORTS = {
    20, 21, 22, 23, 25, 53, 67, 68, 69, 80, 110, 111, 123, 137, 138, 139, 143,
    161, 162, 389, 443, 445, 465, 514, 587, 993, 995, 1080, 1194, 1433, 1521,
    2049, 2375, 2376, 3000, 3128, 3306, 3389, 4000, 4444, 5000, 5432, 5601,
    5900, 5985, 5986, 6379, 6443, 6667, 8000, 8001, 8008, 8080, 8081, 8443,
    9000, 9200, 9300, 10000
}


RISKY_SERVICES = {
    "rdp", "smb", "mssql", "mysql", "postgresql", "ssh", "telnet", "vnc",
    "ftp", "http", "https", "ldap", "winrm", "elastic", "redis"
}


def heuristic_severity_for_port(port: PortEntry) -> str:
    sev = "info"
    # Bump severity for uncommon port numbers
    if port.port not in COMMON_PORTS:
        sev = "low"
    # Risky services bump
    svc_name = (port.service.name if port.service else "unknown").lower()
    if any(s in svc_name for s in RISKY_SERVICES):
        sev = max((sev, "medium"), key=lambda s: SEVERITY_ORDER[s])
    # Findings content
    for f in port.scripts:
        text = (f.output or "").lower()
        if "cve-" in text or "vulnerab" in text or "critical" in text:
            return "high"
        if "weak" in text or "insecure" in text:
            sev = max((sev, "medium"), key=lambda s: SEVERITY_ORDER[s])
    return sev


def heuristic_severity_for_finding(f: ScriptFinding) -> str:
    text = (f.output or "").lower() + " " + (f.id or "").lower()
    if "cve-" in text or "critical" in text:
        return "high"
    if "vulnerab" in text or "weak" in text or "insecure" in text:
        return "medium"
    return "info"

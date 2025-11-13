from __future__ import annotations

from typing import Dict, List, Set
from .models import SEVERITY_ORDER, COMMON_PORTS


def parse_csv_set(value: str) -> Set[str]:
    return {v.strip().lower() for v in value.split(',') if v.strip()}


def apply_filters(
    results: Dict,
    min_severity: str | None = None,
    exclude_ports: str | None = None,
    exclude_services: str | None = None,
    only_uncommon_ports: bool = False,
) -> Dict:
    """Filter ports in-place according to provided options and return results."""
    hosts = results.get('hosts', [])
    sev_threshold = SEVERITY_ORDER.get((min_severity or 'info').lower(), 0)
    excl_ports: Set[int] = set()
    if exclude_ports:
        for p in parse_csv_set(exclude_ports):
            try:
                excl_ports.add(int(p))
            except ValueError:
                continue
    excl_services = parse_csv_set(exclude_services) if exclude_services else set()

    for host in hosts:
        filtered_ports = []
        for port in host.get('ports', []):
            try:
                pnum = int(port.get('port')) if isinstance(port.get('port'), str) else int(port.get('port'))
            except Exception:
                pnum = -1

            # Exclude by port number
            if pnum in excl_ports:
                continue

            # Exclude by service name
            svc = (port.get('service') or {}).get('name', '').lower()
            if svc and svc in excl_services:
                continue

            # Only uncommon ports
            if only_uncommon_ports and pnum in COMMON_PORTS:
                continue

            # Severity threshold (port-level severity if present; else derive from scripts)
            port_sev = (port.get('severity') or 'info').lower()
            if SEVERITY_ORDER.get(port_sev, 0) < sev_threshold:
                continue

            filtered_ports.append(port)
        host['ports'] = filtered_ports

    return results

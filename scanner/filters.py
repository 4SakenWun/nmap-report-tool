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


def sort_results(results: Dict, sort_by: str = 'risk') -> Dict:
    """Sort ports within each host by the chosen strategy.

    sort_by options:
      - 'risk': descending by risk_score, then severity, then port
      - 'severity': descending by severity, then risk, then port
      - 'port': ascending by port number
      - 'none': no sorting
    """
    if not results or sort_by == 'none':
        return results

    sev_rank = SEVERITY_ORDER
    for host in results.get('hosts', []):
        ports = host.get('ports', [])
        if sort_by == 'port':
            ports.sort(key=lambda p: int(p.get('port', 0)))
        elif sort_by == 'severity':
            ports.sort(key=lambda p: (
                -sev_rank.get(str(p.get('severity','info')).lower(), 0),
                -int(p.get('risk_score', 0)),
                int(p.get('port', 0))
            ))
        else:  # 'risk' default
            ports.sort(key=lambda p: (
                -int(p.get('risk_score', 0)),
                -sev_rank.get(str(p.get('severity','info')).lower(), 0),
                int(p.get('port', 0))
            ))
        host['ports'] = ports

    return results

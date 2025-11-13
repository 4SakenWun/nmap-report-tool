"""
Nmap scanner module for vulnerability assessment.
Handles target scanning and result parsing.
"""

import subprocess
import io
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import Dict, List, Optional
import platform
import gzip
from .models import (
    Address,
    Service,
    ScriptFinding,
    PortEntry,
    HostEntry,
    ScanResult,
    heuristic_severity_for_finding,
    heuristic_severity_for_port,
    risk_score_for_port,
)


class NmapScanner:
    """Wrapper for nmap scanning operations."""
    
    def __init__(self):
        self.scan_results = {}
        self.scan_timestamp = None
        
    def check_nmap_installed(self) -> bool:
        """Verify nmap is available on the system."""
        try:
            result = subprocess.run(['nmap', '--version'], 
                                  capture_output=True, 
                                  text=True,
                                  timeout=5)
            return result.returncode == 0
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return False
    
    def scan_target(self, target: str, scan_type: str = 'basic', 
                   ports: Optional[str] = None) -> Dict:
        """
        Execute nmap scan on specified target.
        
        Args:
            target: IP address or hostname to scan
            scan_type: Type of scan (basic, vuln, aggressive)
            ports: Port specification (e.g., '1-1000', '80,443')
            
        Returns:
            Dictionary containing scan results
        """
        if not self.check_nmap_installed():
            raise RuntimeError("nmap is not installed or not in PATH")
        
        # Build nmap command based on scan type
        cmd = ['nmap']
        
        if scan_type == 'basic':
            cmd.extend(['-sV', '-sC'])  # version detection + default scripts
        elif scan_type == 'vuln':
            cmd.extend(['-sV', '--script=vuln'])  # vulnerability scripts
        elif scan_type == 'aggressive':
            cmd.extend(['-A'])  # aggressive scan
        else:
            cmd.extend(['-sV'])  # default to version detection
        
        # Add port specification if provided
        if ports:
            cmd.extend(['-p', ports])
        
        # Output format for easier parsing
        cmd.extend(['-oX', '-'])  # XML output to stdout
        cmd.append(target)
        
        try:
            self.scan_timestamp = datetime.now()
            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=300
            )  # 5 min timeout

            if result.returncode != 0:
                raise RuntimeError(f"Nmap scan failed: {result.stderr}")

            # Parse XML output with streaming iterparse
            scan_result = self._parse_xml_output(result.stdout, target)
            self.scan_results = scan_result.to_dict()
            return self.scan_results

        except subprocess.TimeoutExpired:
            raise RuntimeError("Scan timed out after 5 minutes")
        except Exception as e:
            raise RuntimeError(f"Scan error: {str(e)}")
    
    def _parse_xml_output(self, xml_data: str, target: str) -> ScanResult:
        """Parse nmap XML output into structured dataclasses using iterparse."""
        try:
            # iterparse expects a file-like
            f = io.StringIO(xml_data)
            context = ET.iterparse(f, events=("start", "end"))
            _, root = next(context)  # get root element

            scanner_version = root.get("version", "Unknown")
            hosts: List[HostEntry] = []
            
            for event, elem in context:
                if event == "end" and elem.tag == "host":
                    host_data = self._parse_host(elem)
                    if host_data:
                        hosts.append(host_data)
                    # clear processed element to save memory
                    root.remove(elem)

            result = ScanResult(
                target=target,
                scan_time=self.scan_timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                scanner_version=scanner_version,
                hosts=hosts,
            )
            # Compute total risk
            result.total_risk = sum(getattr(h, 'risk_score', 0) for h in hosts)
            return result

        except ET.ParseError as e:
            raise RuntimeError(f"Failed to parse nmap output: {str(e)}")

    def parse_xml_file(self, file_path: str, target: Optional[str] = None) -> Dict:
        """Parse an existing nmap XML file (supports .gz). Useful for offline analysis/tests."""
        try:
            if file_path.endswith('.gz'):
                with gzip.open(file_path, 'rt', encoding='utf-8') as f:
                    xml_data = f.read()
            else:
                with open(file_path, 'r', encoding='utf-8') as f:
                    xml_data = f.read()

            # Use provided target or derive from file name
            tgt = target or 'offline'
            self.scan_timestamp = datetime.now()
            scan_result = self._parse_xml_output(xml_data, tgt)
            self.scan_results = scan_result.to_dict()
            return self.scan_results
        except Exception as e:
            raise RuntimeError(f"Failed to parse XML file '{file_path}': {e}")
    
    def _parse_host(self, host_elem) -> Optional[HostEntry]:
        """Extract host information from XML element."""
        # Check if host is up
        status = host_elem.find('status')
        if status is None or status.get('state') != 'up':
            return None
        
        host_addrs: List[Address] = []
        hostnames: List[str] = []
        ports: List[PortEntry] = []
        host_os = None
        
        # Get addresses
        for addr in host_elem.findall('address'):
            addr_type = addr.get('addrtype', 'unknown')
            addr_val = addr.get('addr', '')
            host_addrs.append(Address(type=addr_type, address=addr_val))
        
        # Get hostnames
        hostnames_elem = host_elem.find('hostnames')
        if hostnames_elem is not None:
            for hostname in hostnames_elem.findall('hostname'):
                hostnames.append(hostname.get('name', ''))
        
        # Get port information
        ports_elem = host_elem.find('ports')
        if ports_elem is not None:
            for port in ports_elem.findall('port'):
                port_data = self._parse_port(port)
                if port_data:
                    ports.append(port_data)
        
        # Get OS detection if available
        os_elem = host_elem.find('os')
        if os_elem is not None:
            osmatch = os_elem.find('osmatch')
            if osmatch is not None:
                host_os = {
                    'name': osmatch.get('name', 'Unknown'),
                    'accuracy': osmatch.get('accuracy', '0')
                }

        host_entry = HostEntry(
            status='up',
            addresses=host_addrs,
            hostnames=hostnames,
            ports=ports,
            os=host_os
        )
        # Compute host risk from ports
        host_entry.risk_score = sum(getattr(p, 'risk_score', 0) for p in ports)
        return host_entry
    
    def _parse_port(self, port_elem) -> Optional[PortEntry]:
        """Extract port information from XML element."""
        state = port_elem.find('state')
        if state is None or state.get('state') != 'open':
            return None
        
        port_id = int(port_elem.get('portid', '0') or 0)
        protocol = port_elem.get('protocol', '')
        port_service: Optional[Service] = None
        findings: List[ScriptFinding] = []
        
        # Get service information
        service = port_elem.find('service')
        if service is not None:
            port_service = Service(
                name=service.get('name', 'unknown'),
                product=service.get('product', ''),
                version=service.get('version', ''),
                extrainfo=service.get('extrainfo', ''),
            )
        
        # Get script output (vulnerabilities, etc.)
        for script in port_elem.findall('script'):
            sf = ScriptFinding(
                id=script.get('id', ''),
                output=script.get('output', '')
            )
            sf.severity = heuristic_severity_for_finding(sf)
            findings.append(sf)

        # Build port entry and compute severity
        pe = PortEntry(
            port=port_id,
            protocol=protocol,
            state=state.get('state', ''),
            service=port_service,
            scripts=findings,
        )
        pe.severity = heuristic_severity_for_port(pe)
        pe.risk_score = risk_score_for_port(pe)
        return pe
    
    def get_summary(self) -> Dict:
        """Generate a summary of scan results."""
        if not self.scan_results:
            return {'error': 'No scan results available'}
        
        total_hosts = len(self.scan_results.get('hosts', []))
        total_open_ports = sum(
            len(host.get('ports', [])) 
            for host in self.scan_results.get('hosts', [])
        )
        
        # Count vulnerabilities (scripts with 'vuln' in name)
        vuln_count = 0
        for host in self.scan_results.get('hosts', []):
            for port in host.get('ports', []):
                for script in port.get('scripts', []):
                    if 'vuln' in script.get('id', '').lower():
                        vuln_count += 1
        
        return {
            'target': self.scan_results.get('target', 'Unknown'),
            'scan_time': self.scan_results.get('scan_time', 'Unknown'),
            'total_hosts': total_hosts,
            'total_open_ports': total_open_ports,
            'potential_vulnerabilities': vuln_count
        }

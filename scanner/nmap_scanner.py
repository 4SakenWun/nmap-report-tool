"""
Nmap scanner module for vulnerability assessment.
Handles target scanning and result parsing.
"""

import subprocess
import json
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import Dict, List, Optional
import platform


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
            result = subprocess.run(cmd, 
                                  capture_output=True, 
                                  text=True,
                                  timeout=300)  # 5 min timeout
            
            if result.returncode != 0:
                raise RuntimeError(f"Nmap scan failed: {result.stderr}")
            
            # Parse XML output
            self.scan_results = self._parse_xml_output(result.stdout, target)
            return self.scan_results
            
        except subprocess.TimeoutExpired:
            raise RuntimeError("Scan timed out after 5 minutes")
        except Exception as e:
            raise RuntimeError(f"Scan error: {str(e)}")
    
    def _parse_xml_output(self, xml_data: str, target: str) -> Dict:
        """Parse nmap XML output into structured data."""
        try:
            root = ET.fromstring(xml_data)
            
            results = {
                'target': target,
                'scan_time': self.scan_timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                'scanner_version': root.get('version', 'Unknown'),
                'hosts': []
            }
            
            # Parse each host
            for host in root.findall('host'):
                host_data = self._parse_host(host)
                if host_data:
                    results['hosts'].append(host_data)
            
            return results
            
        except ET.ParseError as e:
            raise RuntimeError(f"Failed to parse nmap output: {str(e)}")
    
    def _parse_host(self, host_elem) -> Optional[Dict]:
        """Extract host information from XML element."""
        # Check if host is up
        status = host_elem.find('status')
        if status is None or status.get('state') != 'up':
            return None
        
        host_data = {
            'status': 'up',
            'addresses': [],
            'hostnames': [],
            'ports': [],
            'os': None
        }
        
        # Get addresses
        for addr in host_elem.findall('address'):
            addr_type = addr.get('addrtype', 'unknown')
            addr_val = addr.get('addr', '')
            host_data['addresses'].append({
                'type': addr_type,
                'address': addr_val
            })
        
        # Get hostnames
        hostnames_elem = host_elem.find('hostnames')
        if hostnames_elem is not None:
            for hostname in hostnames_elem.findall('hostname'):
                host_data['hostnames'].append(hostname.get('name', ''))
        
        # Get port information
        ports_elem = host_elem.find('ports')
        if ports_elem is not None:
            for port in ports_elem.findall('port'):
                port_data = self._parse_port(port)
                if port_data:
                    host_data['ports'].append(port_data)
        
        # Get OS detection if available
        os_elem = host_elem.find('os')
        if os_elem is not None:
            osmatch = os_elem.find('osmatch')
            if osmatch is not None:
                host_data['os'] = {
                    'name': osmatch.get('name', 'Unknown'),
                    'accuracy': osmatch.get('accuracy', '0')
                }
        
        return host_data
    
    def _parse_port(self, port_elem) -> Optional[Dict]:
        """Extract port information from XML element."""
        state = port_elem.find('state')
        if state is None or state.get('state') != 'open':
            return None
        
        port_data = {
            'port': port_elem.get('portid', ''),
            'protocol': port_elem.get('protocol', ''),
            'state': state.get('state', ''),
            'service': None,
            'scripts': []
        }
        
        # Get service information
        service = port_elem.find('service')
        if service is not None:
            port_data['service'] = {
                'name': service.get('name', 'unknown'),
                'product': service.get('product', ''),
                'version': service.get('version', ''),
                'extrainfo': service.get('extrainfo', '')
            }
        
        # Get script output (vulnerabilities, etc.)
        for script in port_elem.findall('script'):
            script_data = {
                'id': script.get('id', ''),
                'output': script.get('output', '')
            }
            port_data['scripts'].append(script_data)
        
        return port_data
    
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

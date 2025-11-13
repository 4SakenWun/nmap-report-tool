#!/usr/bin/env python3
"""
Nmap Vulnerability Scanner and Report Generator
A tool for penetration testers to scan targets and generate professional reports.

================================================================================
                            LEGAL WARNING
                                                                              
  This tool is for AUTHORIZED SECURITY TESTING ONLY.
                                                                              
  By using this software, you certify that:
  - You have EXPLICIT WRITTEN PERMISSION to scan the target system
  - You understand unauthorized access is ILLEGAL and may result in
    criminal prosecution and imprisonment
  - You accept FULL RESPONSIBILITY for all actions performed with this tool
                                                                              
  Unauthorized scanning is a violation of:
  - Computer Fraud and Abuse Act (CFAA) - USA
  - Computer Misuse Act - UK
  - Similar laws in other jurisdictions
                                                                              
  The author accepts NO LIABILITY for misuse of this software.
================================================================================
"""

import argparse
import sys
import os
from datetime import datetime
from scanner.nmap_scanner import NmapScanner
from reports.report_generator import ReportGenerator
from scanner.filters import apply_filters
from app_version import __version__


def print_banner():
    """Display legal warning banner."""
    banner = """
================================================================================
               Nmap Vulnerability Scanner & Report Generator
                    For Authorized Use Only - CEH Edition
================================================================================

WARNING: Ensure you have explicit written authorization before scanning any target.
         Unauthorized scanning may be illegal in your jurisdiction.
"""
    print(banner)


def verify_authorization():
    """Prompt user to confirm they have authorization."""
    print("AUTHORIZATION CHECK")
    print("-" * 80)
    response = input("Do you have WRITTEN AUTHORIZATION to scan this target? (yes/no): ").strip().lower()
    
    if response not in ['yes', 'y']:
        print("\n⚠️  SCAN ABORTED: You must have written authorization to proceed.")
        print("   Only scan systems you own or have explicit permission to test.")
        sys.exit(0)
    
    print("✓ Authorization confirmed. Proceeding with scan...")
    print("-" * 80)
    print()


def main():
    """Main entry point for the scanner application."""
    # Display banner
    print_banner()
    
    parser = argparse.ArgumentParser(
        description='Nmap vulnerability scanner with automated report generation',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  Basic scan with PDF report:
    python main.py -t 192.168.1.1 -o report.pdf
  
  Vulnerability scan with DOCX report:
    python main.py -t scanme.nmap.org -s vuln -o report.docx
  
  Aggressive scan on specific ports:
    python main.py -t 10.0.0.1 -s aggressive -p 80,443,8080 -o scan_results.pdf

LEGAL REMINDER:
  You must have explicit written authorization to scan any target.
  Use --skip-auth-check flag ONLY for authorized lab environments.
        '''
    )
    
    # Provide a standard --version flag
    parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}')
    
    parser.add_argument('-t', '--target', 
                       required=True,
                       help='Target IP address or hostname to scan')
    
    parser.add_argument('-s', '--scan-type',
                       choices=['basic', 'vuln', 'aggressive'],
                       default='basic',
                       help='Type of scan to perform (default: basic)')
    
    parser.add_argument('-p', '--ports',
                       help='Port specification (e.g., 1-1000, 80,443,8080)')
    
    parser.add_argument('-o', '--output',
                       required=True,
                       help='Output file path. Extension may be overridden by --format.')

    parser.add_argument('--format',
                       choices=['pdf', 'docx', 'txt', 'html', 'md', 'json'],
                       help='Explicit output format (overrides output file extension)')
    
    parser.add_argument('-v', '--verbose',
                       action='store_true',
                       help='Enable verbose output')
    
    parser.add_argument('--skip-auth-check',
                       action='store_true',
                       help='Skip authorization prompt (use only for authorized lab environments)')

    # Filtering options
    parser.add_argument('--min-severity',
                       choices=['info', 'low', 'medium', 'high', 'critical'],
                       help='Minimum severity to include in reports')
    parser.add_argument('--exclude-ports',
                       help='Comma-separated list of ports to exclude (e.g., 22,3389)')
    parser.add_argument('--exclude-services',
                       help='Comma-separated list of service names to exclude (e.g., ssh,rdp,smb)')
    parser.add_argument('--only-uncommon-ports',
                       action='store_true',
                       help='Include only uncommon ports (excludes well-known/common ports)')
    
    args = parser.parse_args()
    
    # Verify authorization unless skipped
    if not args.skip_auth_check:
        verify_authorization()
    
    # Determine output format
    requested_fmt = args.format
    output_path = args.output
    base, ext = os.path.splitext(output_path)
    ext = ext.lower()
    if requested_fmt:
        desired_ext = f".{requested_fmt.lower()}"
        if ext != desired_ext:
            # Replace or append extension to match requested format
            output_path = base + desired_ext
        output_ext = desired_ext
    else:
        output_ext = ext if ext in ['.pdf', '.docx', '.txt', '.html', '.md', '.json'] else ''
        if not output_ext:
            print("Error: Could not determine output format. Provide a supported extension or use --format.")
            sys.exit(1)
    
    # Initialize scanner
    scanner = NmapScanner()
    
    # Check if nmap is installed
    if not scanner.check_nmap_installed():
        print("Error: nmap is not installed or not found in PATH")
        print("Please install nmap:")
        print("  - Linux: sudo apt-get install nmap")
        print("  - macOS: brew install nmap")
        print("  - Windows: Download from https://nmap.org/download.html")
        sys.exit(1)
    
    print(f"Starting {args.scan_type} scan on target: {args.target}")
    if args.ports:
        print(f"Scanning ports: {args.ports}")
    print("This may take a few minutes...\n")
    
    try:
        # Run the scan
        results = scanner.scan_target(
            target=args.target,
            scan_type=args.scan_type,
            ports=args.ports
        )

        # Apply optional filters before generating reports
        if any([args.min_severity, args.exclude_ports, args.exclude_services, args.only_uncommon_ports]):
            results = apply_filters(
                results,
                min_severity=args.min_severity,
                exclude_ports=args.exclude_ports,
                exclude_services=args.exclude_services,
                only_uncommon_ports=args.only_uncommon_ports,
            )
        
        if args.verbose:
            summary = scanner.get_summary()
            print("\nScan Summary:")
            print(f"  Target: {summary['target']}")
            print(f"  Scan Time: {summary['scan_time']}")
            print(f"  Hosts Found: {summary['total_hosts']}")
            print(f"  Open Ports: {summary['total_open_ports']}")
            print(f"  Potential Vulnerabilities: {summary['potential_vulnerabilities']}\n")
        
        # Generate report
        print(f"Generating {output_ext[1:].upper()} report...")
        report_gen = ReportGenerator(results)
        
        if output_ext == '.pdf':
            output_file = report_gen.generate_pdf(output_path)
        elif output_ext == '.docx':
            output_file = report_gen.generate_docx(output_path)
        elif output_ext == '.txt':
            output_file = report_gen.generate_text(output_path)
        elif output_ext == '.html':
            output_file = report_gen.generate_html(output_path)
        elif output_ext == '.md':
            output_file = report_gen.generate_markdown(output_path)
        elif output_ext == '.json':
            output_file = report_gen.generate_json(output_path)
        else:
            print("Error: Unsupported output format.")
            sys.exit(1)
        
        print(f"Report generated successfully: {output_file}")
        print(f"\nScan completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
    except RuntimeError as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nScan interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()

import os
from scanner.nmap_scanner import NmapScanner
from scanner.filters import apply_filters

SAMPLES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'samples')
SAMPLE_XML = os.path.join(SAMPLES_DIR, 'nmap_sample.xml')


def test_parse_sample_xml():
    scanner = NmapScanner()
    results = scanner.parse_xml_file(SAMPLE_XML, target='sample')

    assert results['target'] == 'sample'
    assert 'hosts' in results and len(results['hosts']) == 1

    host = results['hosts'][0]
    assert host['status'] == 'up'
    assert len(host['ports']) == 3

    severities = {p['port']: p.get('severity', 'info').lower() for p in host['ports']}
    # Expect http port high due to CVE, ssh medium due to 'weak', 9999 low due to uncommon
    assert severities.get(80) in ('high', 'critical')
    assert severities.get(22) in ('medium', 'high')
    assert severities.get(9999) in ('low', 'medium')

    # Risk scores present
    assert host.get('risk_score', 0) > 0
    assert results.get('total_risk', 0) >= host['risk_score']


def test_filters_reduce_ports():
    scanner = NmapScanner()
    results = scanner.parse_xml_file(SAMPLE_XML, target='sample')

    # Min severity medium should drop low-severity uncommon port 9999
    filtered = apply_filters(results, min_severity='medium')
    host = filtered['hosts'][0]
    ports_left = {p['port'] for p in host['ports']}
    assert 9999 not in ports_left
    assert 80 in ports_left and 22 in ports_left

    # Exclude ssh service should remove port 22
    filtered2 = apply_filters(results, exclude_services='ssh')
    ports_left2 = {p['port'] for p in filtered2['hosts'][0]['ports']}
    assert 22 not in ports_left2
    assert 80 in ports_left2

import os
from scanner.nmap_scanner import NmapScanner
from reports.report_generator import ReportGenerator

SAMPLES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'samples')
SAMPLE_XML = os.path.join(SAMPLES_DIR, 'nmap_sample.xml')


def test_generate_markdown_and_html(tmp_path):
    scanner = NmapScanner()
    results = scanner.parse_xml_file(SAMPLE_XML, target='sample')

    rg = ReportGenerator(results)

    md_path = tmp_path / 'report.md'
    html_path = tmp_path / 'report.html'

    rg.generate_markdown(str(md_path))
    rg.generate_html(str(html_path))

    md = md_path.read_text(encoding='utf-8')
    html = html_path.read_text(encoding='utf-8')

    # Basic checks for content
    assert 'Vulnerability Scan Report' in md
    assert '| Severity | Count |' in md
    assert 'Total Risk Score:' in md
    assert '**Host Risk Score:**' in md

    assert '<h1>Vulnerability Scan Report</h1>' in html
    assert '<table' in html and 'Severity' in html
    assert 'Total Risk Score:' in html
    assert 'Risk Score:' in html

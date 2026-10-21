#!/usr/bin/env python3
"""Correlate available Scenario B security evidence."""

import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / "security-evidence"
OUTPUT = EVIDENCE / "correlation"
OUTPUT.mkdir(parents=True, exist_ok=True)


def read_json(path):
    try:
        with path.open(encoding="utf-8") as file:
            return json.load(file)
    except (OSError, json.JSONDecodeError):
        return None


def read_json_lines(path):
    rows = []
    try:
        with path.open(encoding="utf-8") as file:
            for line in file:
                if line.strip():
                    try:
                        rows.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
    except OSError:
        pass
    return rows


def file_info(path):
    if not path.is_file():
        return {"path": str(path.relative_to(ROOT)), "exists": False}
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    return {
        "path": str(path.relative_to(ROOT)),
        "exists": True,
        "size_bytes": path.stat().st_size,
        "sha256": digest,
    }


zap_path = EVIDENCE / "security-scans/zap-final-login-alerts.json"
selenium_path = EVIDENCE / "selenium/selenium-browser-test.json"
suricata_path = EVIDENCE / "suricata/eve.json"
trivy_path = EVIDENCE / "security-scans/trivy-juice-shop.json"
sbom_path = EVIDENCE / "security-scans/juice-shop-sbom.cyclonedx.json"
pcap_path = ROOT / "packet-captures/scenario-b-sqli-final.pcapng"

zap = read_json(zap_path)
selenium = read_json(selenium_path)
suricata_events = read_json_lines(suricata_path)
trivy = read_json(trivy_path)
sbom = read_json(sbom_path)

zap_alerts = []
if isinstance(zap, dict):
    zap_alerts = zap.get("alerts", [])
elif isinstance(zap, list):
    zap_alerts = zap

zap_sqli = [
    alert for alert in zap_alerts
    if "40018" in str(alert.get("pluginid", alert.get("pluginId", "")))
    or "SQL Injection" in str(alert.get("name", ""))
]

suricata_alerts = [
    event for event in suricata_events
    if event.get("event_type") == "alert"
    and event.get("alert", {}).get("signature_id") == 1000001
]

trivy_counts = {}
misconfig_count = 0
secret_count = 0
if isinstance(trivy, dict):
    for result in trivy.get("Results", []):
        for item in result.get("Vulnerabilities") or []:
            severity = item.get("Severity", "UNKNOWN")
            trivy_counts[severity] = trivy_counts.get(severity, 0) + 1
        misconfig_count += len(result.get("Misconfigurations") or [])
        secret_count += len(result.get("Secrets") or [])

components = sbom.get("components", []) if isinstance(sbom, dict) else []

evidence_files = [
    zap_path, selenium_path, pcap_path, suricata_path, trivy_path, sbom_path
]

report = {
    "generated_utc": datetime.now(timezone.utc).isoformat(),
    "project": "Telecommunications Security, DevSecOps, and Traffic Intelligence",
    "scenario": "B",
    "status": "EVIDENCE_PARTIAL",
    "correlation_note": (
        "This report summarizes separately collected artifacts. "
        "Matching indicators do not prove all tests occurred in one session."
    ),
    "observations": {
        "zap": {
            "evidence": file_info(zap_path),
            "sql_injection_alerts_found": len(zap_sqli),
            "alert_ids": [
                alert.get("pluginid", alert.get("pluginId"))
                for alert in zap_sqli
            ],
        },
        "selenium": {
            "evidence": file_info(selenium_path),
            "test_status": selenium.get("status") if isinstance(selenium, dict) else None,
            "page_loaded": selenium.get("page_loaded") if isinstance(selenium, dict) else None,
            "test_scope": "Browser smoke test; not an authentication test",
        },
        "packet_capture": {
            "evidence": file_info(pcap_path),
            "expected_test_uri": "/rest/products/search?q=test%27%28",
            "pcap_request_verified_separately_with_tshark": pcap_path.is_file(),
        },
        "suricata": {
            "evidence": file_info(suricata_path),
            "local_sid_1000001_alert_count": len(suricata_alerts),
            "alerts": [
                {
                    "signature": event.get("alert", {}).get("signature"),
                    "source_ip": event.get("src_ip"),
                    "destination_ip": event.get("dest_ip"),
                }
                for event in suricata_alerts
            ],
        },
        "trivy": {
            "evidence": file_info(trivy_path),
            "vulnerability_counts_by_severity": trivy_counts,
            "misconfiguration_findings": misconfig_count,
            "secret_findings": secret_count,
            "note": "Scanner findings are not automatically confirmed exploitable.",
        },
        "sbom": {
            "evidence": file_info(sbom_path),
            "format": sbom.get("bomFormat") if isinstance(sbom, dict) else None,
            "component_count": len(components),
        },
    },
    "artifact_manifest": [file_info(path) for path in evidence_files],
    "security_gate": {
        "mode": "REPORT_ONLY",
        "decision": "NOT_EVALUATED",
        "note": "This correlation script does not implement the Jenkins security gate.",
    },
}

(OUTPUT / "security-event-correlation.json").write_text(
    json.dumps(report, indent=2) + "\n", encoding="utf-8"
)

lines = [
    "# Scenario B Security Evidence Correlation",
    "",
    f"Generated (UTC): {report['generated_utc']}",
    "",
    f"**Evidence status:** {report['status']}",
    "",
    "## Findings",
    "",
    f"- ZAP SQL injection alerts in selected export: **{len(zap_sqli)}**",
    f"- Selenium browser test: **{report['observations']['selenium']['test_status'] or 'UNKNOWN'}**",
    f"- Suricata SID 1000001 alerts: **{len(suricata_alerts)}**",
    f"- Trivy vulnerability counts: `{json.dumps(trivy_counts, sort_keys=True)}`",
    f"- Trivy misconfiguration findings: **{misconfig_count}**",
    f"- Trivy secret findings: **{secret_count}**",
    f"- SBOM components: **{len(components)}**",
    "",
    "## Evidence limitations",
    "",
    "- The PCAP is a controlled product-search test, not the separate login SQL injection test.",
    "- The Selenium test is a browser smoke test, not an authentication test.",
    "- Evidence files may come from separate runs; this report does not claim a single-session causal chain.",
    "- Trivy findings require triage and are not all proof of exploitability.",
    "- The Jenkins security gate has not been evaluated by this script.",
    "",
    "## Artifact integrity",
    "",
    "| Artifact | Exists | Size (bytes) | SHA-256 |",
    "|---|---:|---:|---|",
]

for item in report["artifact_manifest"]:
    lines.append(
        f"| `{item['path']}` | {item['exists']} | "
        f"{item.get('size_bytes', '')} | `{item.get('sha256', '')}` |"
    )

(OUTPUT / "security-event-correlation.md").write_text(
    "\n".join(lines) + "\n", encoding="utf-8"
)

print("Correlation reports created:")
print(OUTPUT / "security-event-correlation.json")
print(OUTPUT / "security-event-correlation.md")
print("Evidence status:", report["status"])
print("Suricata SID 1000001 alerts:", len(suricata_alerts))
print("SBOM components:", len(components))

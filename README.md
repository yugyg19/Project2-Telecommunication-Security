# Project 2 — Telecommunications Security, DevSecOps, and Traffic Intelligence

## 1. Project Overview

This project demonstrates a practical security-testing and evidence-analysis workflow for a telecommunications software environment. Scenario B uses OWASP Juice Shop as an intentionally vulnerable web application to demonstrate controlled security testing, packet capture, intrusion detection, vulnerability scanning, software bill of materials generation, and evidence correlation.

The project includes Scenario A materials copied into this repository and Scenario B security-testing evidence.

## 2. Environment

- Operating system: Ubuntu on WSL2
- Container runtime: Docker
- Web application: OWASP Juice Shop `bkimminich/juice-shop:v20.2.0`
- Dynamic security testing: OWASP ZAP
- Browser testing: Selenium with Chrome Grid
- Packet inspection: TShark
- Network intrusion detection: Suricata
- Vulnerability scanning: Trivy
- SBOM generation: Syft
- Evidence processing: Python
- CI/CD pipeline definition: Jenkinsfile

Tool versions and container status should be verified in the environment used for a future reproduction.

## 3. Scenario B Workflow

1. Check the application and testing environment.
2. Run ZAP baseline and targeted security testing.
3. Run a Selenium browser smoke test against Juice Shop.
4. Capture controlled HTTP traffic in a PCAP file.
5. Analyze the capture with TShark.
6. Run Suricata against the captured traffic using a local test rule.
7. Scan the Juice Shop image with Trivy.
8. Generate a CycloneDX SBOM using Syft.
9. Correlate available evidence into JSON and Markdown reports.
10. Use the Jenkinsfile to define validation, evidence correlation, security-gate, and artifact-archiving stages.

## 4. Important Evidence

| Artifact | Location |
|---|---|
| ZAP baseline report | `security-evidence/security-scans/zap-baseline-report.html` |
| ZAP baseline JSON | `security-evidence/security-scans/zap-baseline-report.json` |
| Selenium browser test | `security-evidence/selenium/selenium-browser-test.json` |
| Selenium screenshot | `screenshots/juice-shop-selenium.png` |
| Controlled SQLi PCAP | `packet-captures/scenario-b-sqli-final.pcapng` |
| Suricata EVE JSON | `security-evidence/suricata/eve.json` |
| Trivy report | `security-evidence/security-scans/trivy-juice-shop.json` |
| CycloneDX SBOM | `security-evidence/security-scans/juice-shop-sbom.cyclonedx.json` |
| Correlation JSON | `security-evidence/correlation/security-event-correlation.json` |
| Correlation Markdown | `security-evidence/correlation/security-event-correlation.md` |

## 5. Reproducing the Evidence Correlation

From the repository root, create or activate a Python environment with the required Python dependencies, including Selenium for the browser test.

To validate and regenerate the evidence-correlation reports:

```bash
python3 -m py_compile scenario-b/correlation/correlate_evidence.py
python3 scenario-b/correlation/correlate_evidence.py
python3 -m json.tool security-evidence/correlation/security-event-correlation.json
```

The correlation script summarizes existing evidence. It does not itself rerun ZAP, Trivy, Syft, or Suricata.

## 6. Controlled SQL Injection Test and Limitations

Juice Shop is intentionally vulnerable and is used only as a controlled lab target. The captured product-search request contains the URI:

`/rest/products/search?q=test%27%28`

The local Suricata rule uses SID `1000001` to detect this specific test request. It is a narrowly scoped positive-control rule, not a general-purpose SQL injection detector.

The ZAP login SQL injection evidence and the product-search PCAP are separate test artifacts. They must not be described as one request or one session.

## 7. Vulnerability Scan and SBOM

Trivy findings are scanner results requiring triage; they do not automatically establish that every reported issue is exploitable. The Syft output records components identified in the scanned image. Both outputs should be retained as evidence and reviewed alongside the image version.

## 8. Jenkins Pipeline Status

The repository contains a `Jenkinsfile` defining preflight checks, evidence validation, Selenium testing, evidence correlation, a security gate, and artifact archiving.

The pipeline has received basic file-structure checks, and its local gate logic has been checked against the saved correlation report. A full Jenkins execution has not yet been verified. The `REPORT_ONLY` and `ENFORCE` modes must be tested in a working Jenkins environment before claiming that the CI/CD pipeline is fully operational.

## 9. Evidence Limitations

- The correlation report summarizes artifacts collected at different times and does not prove that all tests occurred in one session.
- The Selenium test is a browser smoke test, not a complete authentication test.
- Four additional packet-capture files were found to contain zero packets and should not be treated as successful captures.
- The controlled PCAP and the ZAP login SQL injection evidence represent separate tests.
- The security-gate decision and final Jenkins build result remain unverified until Jenkins actually runs the pipeline.

## 10. Safety and Scope

Perform security tests only against the intentionally vulnerable lab application and authorized environments. Do not reuse test credentials or tokens outside the lab. Review files for secrets and sensitive traffic before publishing this repository.

## 11. Repository Structure

- `scenario-a/` — Scenario A project materials
- `scenario-b/` — Scenario B test scripts, ZAP plan, and correlation script
- `security-evidence/` — Scan reports, browser evidence, Suricata output, and correlation reports
- `packet-captures/` — Packet-capture evidence
- `screenshots/` — Screenshots for the project
- `security/` — Local Suricata rules
- `analysis/`, `measurements/`, `logs/`, `report/`, and `presentation/` — Supporting project materials

## 12. Current Completion Status

Scenario B evidence collection and local evidence correlation have been performed. Documentation and repository review are in progress. Full Jenkins execution, testing of both gate modes in Jenkins, and final GitHub publication remain pending.

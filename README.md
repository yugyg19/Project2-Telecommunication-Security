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
| Controlled SQLi PCAP (fresh capture) | `security-evidence/fresh-capture-20261027/sqli-product-search-corrected.pcap` |
| Suricata EVE JSON (fresh offline analysis) | `security-evidence/fresh-capture-20261027/suricata-no-checksum/eve.json` |
| Trivy report (fresh scan) | `security-evidence/security-scans/trivy-juice-shop-fresh.json` |
| CycloneDX SBOM (fresh generation) | `security-evidence/security-scans/juice-shop-sbom-fresh.cyclonedx.json` |
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

The Jenkins pipeline has been configured and its work has been completed in the project environment, as recorded by the project author. The `Jenkinsfile` defines preflight checks, evidence validation, Selenium testing, evidence correlation, security-gate handling, and artifact archiving. The `REPORT_ONLY` and `ENFORCE` modes have different purposes: reporting findings does not necessarily mean the build is blocked. Consult the saved build output and archived artifacts for the exact result of each run.

## 9. Evidence Limitations and Interpretation

- The correlation report combines evidence collected at different times; it does not prove that all observations came from one session.
- The Selenium browser smoke test demonstrates basic browser access, not complete application security or authentication coverage.
- The targeted ZAP login test and the controlled product-search PCAP are separate tests. The ZAP finding is an alert requiring manual validation, not proof by itself that SQL injection is exploitable.
- The local Suricata SID `1000001` is a narrowly scoped positive-control rule. Its alert indicates detection; it does not block traffic.
- The fresh Trivy report records scanner findings that require triage. Findings do not automatically establish exploitability.
- The fresh SBOM records components identified in the scanned image; it is not, by itself, a vulnerability assessment.
- The 5G application-path evidence records successful UE connectivity, an HTTP redirect to HTTPS, and an HTTPS 200 response with security headers. The HTTPS request used `curl -k`, so certificate trust validation was not verified.
- Offline Suricata analysis used `-k none`, disabling checksum validation for that analysis. This should be disclosed when interpreting the packet-capture results.
- Empty packet captures and historical test results should not be presented as successful fresh tests.

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

The project implementation, security-evidence collection, local evidence correlation, and Jenkins work have been completed in the project environment as recorded by the project author. Fresh Trivy, SBOM, packet-capture, Suricata, and 5G application-path evidence is documented above. The correlation status may remain `EVIDENCE_PARTIAL` because the evidence was collected across separate runs; this is a limitation of evidence correlation, not a claim that every individual test failed.

Before submission, verify that the intended source files and evidence are committed and pushed to the intended GitHub repository. Do not commit credentials, tokens, private keys, unrelated local workspace data, or unnecessary backup files.

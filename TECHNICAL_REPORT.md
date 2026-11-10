# PROJECT 2: TELECOMMUNICATION SECURITY, DEVSECOPS, AND TRAFFIC INTELLIGENCE
**Technical Report**

**Repository:** https://github.com/yugyg19/Project2-Telecommunication-Security  
**Branch:** `main`  
**Latest recorded commit:** `0b7162eda4620dceb891cda2c8b8c5d3bfb781f9`

---

## Abstract
Project 2 extends a Docker-based software telecommunications environment with application security, automated security testing, network traffic inspection, intrusion-detection analysis, software vulnerability assessment, software-bill-of-materials generation, evidence correlation, and a Jenkins-based workflow. Scenario A establishes a secure application service connected through the 5G user-plane path. Scenario B adds an isolated OWASP Juice Shop testing environment and supporting DevSecOps tools.

The recorded implementation demonstrates successful 5G UE registration and PDU-session establishment, a working UE tunnel interface, connectivity through the tunnel, an HTTP-to-HTTPS redirect, and an HTTPS HTTP 200 response with security headers. Scenario B evidence includes Selenium browser testing, ZAP testing, a fresh packet capture, offline Suricata analysis, Trivy scanning, a CycloneDX SBOM, TShark summaries, and Python-generated correlation reports. Selected implementation files and evidence were pushed to GitHub.

This report distinguishes observed results from limitations. The HTTPS request used `curl -k`, so certificate-chain trust was not validated by that request. Offline Suricata analysis used `-k none`, so checksum validation was disabled. The evidence spans separate test runs; the correlation output is marked `EVIDENCE_PARTIAL` rather than claiming all observations belong to one fully correlated Jenkins execution.

## 1. Introduction
The purpose of Project 2 is to extend the Project 1 5G Standalone laboratory environment into a security-focused environment. The work follows the sequence:

**Reuse → Secure → Model → Test → Detect → Automate → Analyze → Defend**

Scenario A provides the secure application baseline. Scenario B provides the security-testing and evidence-processing workflow around a deliberately vulnerable training application. OWASP Juice Shop is isolated from the secure Scenario A Django/Nginx application and is used only as an authorized laboratory target.

## 2. Objectives
1. Reuse the existing Docker-based 5G Standalone environment and verify UE connectivity.
2. Deploy and secure a Django application behind an Nginx reverse proxy.
3. Demonstrate HTTP redirection, HTTPS delivery, authentication-related controls, CSRF enforcement, secure cookies, HSTS, and security headers where verified.
4. Establish an isolated security-testing environment containing OWASP Juice Shop and Selenium Grid.
5. Use OWASP ZAP and Selenium to assess application behavior and security.
6. Generate controlled SQL-injection test traffic and capture packets for offline analysis.
7. Use Suricata to identify the configured local positive-control traffic signature.
8. Use Trivy to produce a vulnerability report and Syft to generate a CycloneDX SBOM.
9. Inspect packet evidence with TShark and process structured evidence with `jq` and Python.
10. Produce evidence-correlation reports and use Jenkins to orchestrate the workflow.

## 3. Scope and Architecture

### 3.1 Scenario A — Secure application service
The project guide defines the application path as:

`UE → gNB → N3/GTP-U → UPF → N6 → Nginx → Django`

Nginx acts as the reverse proxy and TLS gateway between the N6-facing network and the internal application network. Django is intended to remain on the internal application network rather than being directly exposed to the N6/data network.

The recorded implementation reused the Open5GS/UERANSIM-based 5G environment. UE registration and PDU-session establishment were successful. The UE tunnel interface `uesimtun0` was present with UE address `192.168.100.2`. A connectivity test through the UE tunnel reached the application-side target with four successful ping replies and no packet loss. An HTTP request through the UE network namespace and tunnel returned a redirect to HTTPS. An HTTPS request returned HTTP 200 and security-related response headers.

### 3.2 Scenario B — Security CI/CD and traffic evidence
The recorded environment includes:
- **OWASP Juice Shop:** deliberately vulnerable application used as the controlled target.
- **Selenium Grid:** browser automation and runtime/authentication testing.
- **OWASP ZAP:** baseline and targeted application-security testing.
- **Traffic capture:** packet capture of controlled Juice Shop traffic.
- **Suricata:** offline analysis of the captured PCAP using a local detection rule.
- **TShark:** packet-level inspection and traffic summaries.
- **Trivy:** software/container security scanning.
- **Syft:** software composition inventory and CycloneDX SBOM generation.
- **Python correlation:** combines selected application, network, and software evidence.
- **Jenkins:** pipeline orchestration and security-gate workflow.

These tools have different roles. ZAP produces application-security findings; Suricata produces network detection events; Trivy reports software-security observations; Syft inventories components. A finding from one tool is not interchangeable with another tool's result.

## 4. Implementation and Test Activities

### 4.1 Scenario A: application and gateway security
The Django application was deployed as a containerized service behind Nginx. Django settings were updated with security-related configuration, including secure-cookie settings, HSTS, proxy awareness, and content security policy middleware/configuration.

Recorded checks:
- HTTP on the gateway returned a redirect to HTTPS.
- HTTPS returned HTTP 200.
- Response headers included `X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`, `Referrer-Policy: same-origin`, and `Strict-Transport-Security: max-age=3600`.
- A POST request without a CSRF token returned HTTP 403, demonstrating rejection of that invalid request.
- The UE-to-application path was exercised through the UE tunnel rather than relying only on a direct host-side request.

**Qualification:** the recorded HTTPS tests used `curl -k`, which bypasses certificate verification. They demonstrate HTTPS service availability and response behavior, but do not demonstrate successful validation of the laboratory CA certificate. The project guide specifies a trusted-CA request using `curl --cacert`; that result is not confirmed in the recorded evidence summarized here.

The available record also does not establish every Scenario A acceptance item. A successful authenticated CSRF-protected POST returning HTTP 200, all protected-endpoint authentication/authorization responses, and complete cookie-attribute verification should only be claimed if the corresponding raw test outputs are included.

### 4.2 Scenario B: application security testing
Selenium browser smoke testing completed with a PASS result. A Selenium authentication test result is also present. The authentication test required configured laboratory credentials; its JSON result should be interpreted according to its actual assertions and scope, not as general proof that all authentication controls are secure.

ZAP testing was performed against the controlled Juice Shop application. A targeted test reported a potential SQL-injection finding on `POST /rest/user/login`, parameter `email`, with a quote payload. The reported risk was High and confidence Low, with HTTP 500 and CWE-89. This is a security observation requiring validation; it is not, by itself, proof of exploitable SQL injection.

A separate Jenkins ZAP run was recorded as `NOT_DETECTED` with zero alerts. These outcomes belong to different runs/configurations and must not be combined into one result.

### 4.3 Controlled traffic capture and Suricata
A fresh packet capture was recorded at:

`security-evidence/fresh-capture-20261027/sqli-product-search-corrected.pcap`

The controlled request used the Juice Shop product-search endpoint with a quote/parenthesis test payload. The captured request returned HTTP 500.

Suricata 8.0.3 was run offline against the capture using `security/ids/rules/scenario-b-local.rules`. The offline analysis produced an alert for SID `1000001`, described as a local Scenario B SQL-injection test rule. The event identified traffic from `10.20.10.2` to `10.20.10.20:3000` and an HTTP 500 response.

This rule is a narrowly scoped positive-control signature for the controlled laboratory request. It demonstrates that the configured rule matched the expected test traffic; it is not a general-purpose SQL-injection detector and does not block traffic.

**Checksum limitation:** the offline Suricata invocation used `-k none`, disabling checksum validation for this analysis. This setting must be considered when interpreting the PCAP analysis. The fresh PCAP and the recorded ZAP targeted scan are separate test activities; they should not be represented as the same HTTP transaction unless run identifiers, timestamps, and request details prove that relationship.

### 4.4 Vulnerability scanning and SBOM
Trivy generated a structured vulnerability/security report for the configured Juice Shop target. Syft generated a CycloneDX-compatible SBOM at:

`security-evidence/security-scans/juice-shop-sbom-fresh.cyclonedx.json`

The recorded SBOM contains 2,677 components. The Trivy report is stored at:

`security-evidence/security-scans/trivy-juice-shop-fresh.json`

Trivy findings are observations about the scanned target and scan mode. They are not automatically equivalent to a Jenkins build failure; the configured security-gate policy determines whether a finding changes the build result.

### 4.5 Packet inspection and evidence correlation
TShark-generated traffic summaries are stored under `security-evidence/traffic-analysis/`.

The Python correlation script is `scenario-b/correlation/correlate_evidence.py`. Generated reports:
- `security-evidence/correlation/security-event-correlation.json`
- `security-evidence/correlation/security-event-correlation.md`

The script was updated to reference the fresh PCAP, Suricata EVE output, fresh Trivy report, and SBOM. The generated correlation status is `EVIDENCE_PARTIAL`. This qualification means the evidence was collected across separate executions and does not prove that every artifact belongs to one single end-to-end run. The report does not claim a complete same-run correlation chain where that has not been established.

### 4.6 Jenkins automation
A Jenkins pipeline definition is included in the repository. It describes preflight validation, evidence checks, Selenium testing, correlation, and a security-gate stage. The intended workflow distinguishes:
- **REPORT_ONLY:** configured findings are recorded and archived without enforcing the configured vulnerability threshold as a build failure.
- **ENFORCE:** the configured policy is applied and can reject the build when the threshold is violated.

The repository includes the pipeline definition and evidence files. However, the recorded project notes do not establish a fresh successful end-to-end execution of the final updated Jenkinsfile in both modes. This report therefore does not claim that both modes have been independently revalidated after the final pipeline changes. Use the actual Jenkins console/build record when reporting the final result.

## 5. Test Results Summary

| Area | Recorded result | Interpretation |
|---|---|---|
| 5G UE registration and PDU session | Successful | UE attached and established a PDU session |
| UE tunnel | `uesimtun0` up; UE IP `192.168.100.2` | User-plane interface available |
| UE connectivity | 4/4 ping replies; 0% packet loss | Tested destination reachable through tunnel |
| HTTP gateway behavior | HTTP 301 redirect | HTTP redirected to HTTPS |
| HTTPS application response | HTTP 200 | Service responded over HTTPS; certificate trust not verified because `curl -k` was used |
| Security headers | Headers observed | Header behavior recorded in response |
| Missing-CSRF negative test | HTTP 403 | Invalid/missing CSRF token rejected |
| Selenium browser smoke test | PASS | Browser smoke test passed for its configured scope |
| Targeted ZAP test | Potential SQLi finding; High risk / Low confidence | Requires validation; not proof of exploitability |
| Separate Jenkins ZAP run | NOT_DETECTED; 0 alerts | Separate run; not contradictory to the targeted result |
| Fresh PCAP | Corrected capture recorded | Controlled product-search traffic captured |
| Suricata offline analysis | SID 1000001 alert | Local positive-control rule matched; checksum validation disabled |
| Trivy | Structured JSON report generated | Findings depend on configured scan target and mode |
| Syft | CycloneDX SBOM generated; 2,677 components | Software inventory produced |
| Evidence correlation | `EVIDENCE_PARTIAL` | Evidence exists, but not all is proven to be from one run |
| Jenkins final modes | Final post-update end-to-end result not confirmed | Use actual build records; do not infer success from pipeline-file presence |

## 6. Evidence and Repository Structure

| Evidence | Repository path |
|---|---|
| Main pipeline | `Jenkinsfile` |
| Setup and project instructions | `README.md` |
| Django security settings | `scenario-a/app/project/settings.py` |
| Correlation implementation | `scenario-b/correlation/correlate_evidence.py` |
| Selenium tests | `scenario-b/selenium/` |
| Correlation JSON | `security-evidence/correlation/security-event-correlation.json` |
| Correlation Markdown | `security-evidence/correlation/security-event-correlation.md` |
| 5G application-path note | `security-evidence/final-report/5g-application-path.txt` |
| Fresh corrected PCAP | `security-evidence/fresh-capture-20261027/sqli-product-search-corrected.pcap` |
| Suricata EVE output | `security-evidence/fresh-capture-20261027/suricata-no-checksum/eve.json` |
| Trivy report | `security-evidence/security-scans/trivy-juice-shop-fresh.json` |
| CycloneDX SBOM | `security-evidence/security-scans/juice-shop-sbom-fresh.cyclonedx.json` |
| Selenium authentication result | `security-evidence/selenium/selenium-auth-test.json` |
| TShark summaries | `security-evidence/traffic-analysis/` |
| Local Suricata rule | `security/ids/rules/scenario-b-local.rules` |

The latest recorded commit on `main` is `0b7162eda4620dceb891cda2c8b8c5d3bfb781f9`. Repository: https://github.com/yugyg19/Project2-Telecommunication-Security

## 7. Security, Ethics, and Scope
All security testing described in this report is scoped to the intentionally vulnerable laboratory application and authorized Docker-based test environment. Juice Shop is a training target and must not be treated as a production application. Test credentials and tokens must remain confined to the laboratory.

Before public distribution, the repository should be checked for secrets, private TLS keys, personal credentials, and sensitive traffic. The laboratory CA private key must not be committed. Packet captures may contain application data and should be reviewed before publication.

## 8. Limitations and Future Improvements
1. **Certificate trust:** HTTPS responses were tested using `curl -k`; trusted CA verification using `curl --cacert` is not demonstrated by the recorded result.
2. **Suricata checksum handling:** offline analysis used `-k none`, so checksum validation was disabled.
3. **Evidence correlation:** the correlation report is marked `EVIDENCE_PARTIAL`; artifacts were collected across separate executions and are not claimed to form one complete same-run chain.
4. **ZAP interpretation:** the targeted SQLi observation was High risk but Low confidence and requires manual validation. A separate Jenkins run recorded zero alerts.
5. **Jenkins final verification:** successful end-to-end execution of the final updated pipeline in both `REPORT_ONLY` and `ENFORCE` modes is not established by the recorded evidence summary.
6. **Scenario A acceptance coverage:** a missing-CSRF 403 response and HTTPS response were recorded, but trusted-CA validation and all positive authentication/CSRF acceptance cases should only be claimed when their evidence is available.
7. **Traffic intelligence:** packet inspection and evidence correlation are included. No production-grade machine-learning accuracy or generalized anomaly-detection capability is claimed.

Future improvements include running one uniquely identified Jenkins execution that starts capture before controlled traffic, records all tool outputs under the same run identifier, validates the trusted CA from the UE, completes positive and negative authentication/CSRF tests, and archives the final gate decisions with timestamps and tool versions.

## 9. Conclusion
Project 2 extends the existing 5G laboratory environment with a secure application path and an additional security-testing and DevSecOps layer. The recorded work demonstrates UE registration and connectivity, HTTP-to-HTTPS redirection, an HTTPS application response, security-header observations, a CSRF negative test, browser automation, application-security testing, controlled packet capture, offline Suricata detection, Trivy scanning, SBOM generation, packet inspection, and Python-based evidence correlation.

The report also documents limitations in certificate verification, checksum handling, and cross-run evidence correlation. These qualifications are retained so that the report reflects observed tests rather than unsupported claims. The implementation, selected configurations, scripts, reports, and evidence are published in the GitHub repository above.

## References
1. *Project 2: Telecommunication Security, DevSecOps, and Traffic Intelligence*, course project guide supplied for this project.
2. OWASP Juice Shop — deliberately vulnerable training application used as the Scenario B target.
3. OWASP ZAP — application-security testing tool.
4. Suricata — network threat detection and offline PCAP analysis.
5. Trivy — vulnerability and configuration scanning.
6. Syft — software composition analysis and SBOM generation.
7. TShark — command-line packet analysis.
8. Jenkins — continuous integration and delivery orchestration.

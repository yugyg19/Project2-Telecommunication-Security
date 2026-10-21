# Scenario B Security Evidence Correlation

Generated (UTC): 2026-10-21T13:07:44.694899+00:00

**Evidence status:** EVIDENCE_PARTIAL

## Findings

- ZAP SQL injection alerts in selected export: **1**
- Selenium browser test: **PASS**
- Suricata SID 1000001 alerts: **1**
- Trivy vulnerability counts: `{"CRITICAL": 12, "HIGH": 54, "LOW": 24, "MEDIUM": 86}`
- Trivy misconfiguration findings: **83**
- Trivy secret findings: **6**
- SBOM components: **2677**

## Evidence limitations

- The PCAP is a controlled product-search test, not the separate login SQL injection test.
- The Selenium test is a browser smoke test, not an authentication test.
- Evidence files may come from separate runs; this report does not claim a single-session causal chain.
- Trivy findings require triage and are not all proof of exploitability.
- The Jenkins security gate has not been evaluated by this script.

## Artifact integrity

| Artifact | Exists | Size (bytes) | SHA-256 |
|---|---:|---:|---|
| `security-evidence/security-scans/zap-final-login-alerts.json` | True | 12636 | `e0763b5255814c1c24938e0e2859e7462d78ccd298feeea455ada6a042e36d1d` |
| `security-evidence/selenium/selenium-browser-test.json` | True | 499 | `ecdecb290266aac6c56c3f445adbd0ab0e7f2cb9468107ec1291dafc73d5f59a` |
| `packet-captures/scenario-b-sqli-final.pcapng` | True | 2892 | `b4254efefb8c56dc72bddfa19f8b916f0b761d56d9f057b7144f075327143851` |
| `security-evidence/suricata/eve.json` | True | 21205 | `37dfe2dfa7f99ea958441be7bcd7786a8d0b8934653ef36116ce0f8d75e5fd6c` |
| `security-evidence/security-scans/trivy-juice-shop.json` | True | 1640726 | `034ff5365b88a5ef991de69e6878aedee0a76a9ab4b639a0d4eb083dd7f970b7` |
| `security-evidence/security-scans/juice-shop-sbom.cyclonedx.json` | True | 1507794 | `27d760d561adff64c900f28be0b327300dbfe1565668183756b257d018e9a198` |

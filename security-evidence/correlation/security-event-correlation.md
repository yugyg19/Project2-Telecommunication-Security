# Scenario B Security Evidence Correlation

Generated (UTC): 2026-10-27T08:49:55.509027+00:00

**Evidence status:** EVIDENCE_PARTIAL

## Findings

- ZAP SQL injection alerts in selected export: **1**
- Selenium browser test: **PASS**
- Selenium authentication test: **PASS**
- Historical Selenium authentication test: **FAIL**
- Suricata SID 1000001 alerts: **1**
- Trivy vulnerability counts: `{"CRITICAL": 11, "HIGH": 30, "LOW": 11, "MEDIUM": 52, "UNKNOWN": 1}`
- Trivy misconfiguration findings: **0**
- Trivy secret findings: **0**
- SBOM components: **2677**

## Evidence limitations

- The PCAP is a controlled product-search test, not the separate login SQL injection test.
- The browser smoke test and authentication test are separate test runs.
- The historical authentication failure is retained and is not the latest authentication result.
- Evidence files may come from separate runs; this report does not claim a single-session causal chain.
- Trivy findings require triage and are not all proof of exploitability.
- Jenkins evaluates its security gate after this correlation report is generated; this report does not independently certify the gate result.

## Artifact integrity

| Artifact | Exists | Size (bytes) | SHA-256 |
|---|---:|---:|---|
| `security-evidence/security-scans/zap-final-login-alerts.json` | True | 12636 | `e0763b5255814c1c24938e0e2859e7462d78ccd298feeea455ada6a042e36d1d` |
| `evidence/selenium/selenium-browser-test.json` | True | 453 | `b756ce8835eb83dd39a3b1c23f797a1265b5df30ae7e9180c8e7916f21585024` |
| `evidence/selenium/selenium-auth-test.json` | True | 632 | `bd1886a54c99e13c9a428fdde559f75af89ff153f371dc3362c7c2fcb0d7232f` |
| `security-evidence/selenium/selenium-browser-test.json` | True | 499 | `ecdecb290266aac6c56c3f445adbd0ab0e7f2cb9468107ec1291dafc73d5f59a` |
| `security-evidence/selenium/selenium-auth-test.json` | True | 351 | `f722b152fd8059de96ded94f70a20e36c139469c3a1dc63e26ff35c08c3c88c9` |
| `security-evidence/fresh-capture-20261027/sqli-product-search-corrected.pcap` | True | 2320 | `f445b811d176de82a3341a6f35e674cc84f7021abd58b61d65b463e2e52c46d0` |
| `security-evidence/fresh-capture-20261027/suricata-no-checksum/eve.json` | True | 11193 | `9cc1a46225c3c0e40f437dc8a6af0bd3679cc527a958a7eb2d6ba3cb38ce87bd` |
| `security-evidence/security-scans/trivy-juice-shop-fresh.json` | True | 922757 | `821152208fcd2fc51bffdc7ecc5ad76c650b91662311e72f95ed998c33d15f08` |
| `security-evidence/security-scans/juice-shop-sbom-fresh.cyclonedx.json` | True | 1507794 | `238e7b02186f9950b3110913662049472fd8741f39f75e824f6d82b9fd80d59d` |


pipeline {
    agent any

    parameters {
        choice(
            name: 'SECURITY_GATE_MODE',
            choices: ['REPORT_ONLY', 'ENFORCE'],
            description: 'REPORT_ONLY reports findings; ENFORCE fails on failed required checks.'
        )
    }

    options {
        timestamps()
        disableConcurrentBuilds()
    }

    environment {
        PROJECT_ROOT = '.'
    }

    stages {
        stage('1 - Preflight') {
            steps {
                sh '''
                    set -eu
                    test -f scenario-b/selenium/test_juice_shop.py
                    test -f scenario-b/correlation/correlate_evidence.py
                    test -f security/ids/rules/scenario-b-local.rules
                    test -f packet-captures/scenario-b-sqli-final.pcapng
                    echo "Preflight: PASS"
                '''
            }
        }

        stage('2 - Validate Existing Evidence') {
            steps {
                sh '''
                    set -eu
                    test -s security-evidence/selenium/selenium-browser-test.json
                    test -s security-evidence/suricata/eve.json
                    test -s security-evidence/security-scans/trivy-juice-shop.json
                    test -s security-evidence/security-scans/juice-shop-sbom.cyclonedx.json
                    tshark -r packet-captures/scenario-b-sqli-final.pcapng \
                      -Y 'http.request' \
                      -T fields -e http.request.uri \
                      | grep -F '/rest/products/search?q=test%27%28'
                    echo "Existing evidence: PASS"
                '''
            }
        }

        
        stage('3 - Selenium Browser Test') {
            steps {
                sh '''
                    set -eu
                    python3 -m py_compile scenario-b/selenium/test_juice_shop.py

                    if [ -x .venv/bin/python ]; then
                        PYTHON=.venv/bin/python
                    else
                        PYTHON=python3
                    fi

                    echo "Checking Selenium Grid..."
                    python3 -c "import urllib.request; print(urllib.request.urlopen('http://localhost:4444/status', timeout=5).status)" 

                    echo "Checking Juice Shop..."
                    python3 -c "import urllib.request; print(urllib.request.urlopen('http://10.20.10.20:3000', timeout=5).status)"

                    SELENIUM_GRID_URL=http://localhost:4444 \
                    JUICE_SHOP_URL=http://10.20.10.20:3000 \
                    "$PYTHON" scenario-b/selenium/test_juice_shop.py

                    grep -q '"status": "PASS"' \
                        security-evidence/selenium/selenium-browser-test.json
                    test -s screenshots/juice-shop-selenium.png

                    echo "Selenium browser test: PASS"
                '''
            }
        }


        stage('4 - Correlate Evidence') {
            steps {
                sh '''
                    set -eu
                    python3 -m py_compile scenario-b/correlation/correlate_evidence.py
                    python3 scenario-b/correlation/correlate_evidence.py
                    python3 -m json.tool \
                      security-evidence/correlation/security-event-correlation.json \
                      > /dev/null
                    test -s security-evidence/correlation/security-event-correlation.md
                    echo "Correlation: PASS"
                '''
            }
        }

        stage('5 - Security Gate') {
            steps {
                script {
                    int rc = sh(
                        returnStatus: true,
                        script: '''
                            python3 -c '
import json, sys
from pathlib import Path
p = Path("security-evidence/correlation/security-event-correlation.json")
d = json.loads(p.read_text())
o = d["observations"]
checks = {
    "Selenium PASS": o["selenium"]["test_status"] == "PASS",
    "Suricata positive control": o["suricata"]["local_sid_1000001_alert_count"] > 0,
    "SBOM present": o["sbom"]["component_count"] > 0,
    "PCAP present": o["packet_capture"]["evidence"]["exists"],
}
for name, ok in checks.items():
    print(("PASS" if ok else "FAIL") + ": " + name)
sys.exit(0 if all(checks.values()) else 1)
'
                        '''
                    )

                    if (rc != 0) {
                        if (params.SECURITY_GATE_MODE == 'ENFORCE') {
                            error('Security gate failed in ENFORCE mode')
                        }
                        echo 'REPORT_ONLY: findings recorded; build continues.'
                    } else {
                        echo 'Security gate checks passed.'
                    }
                }
            }
        }
    }

    post {
        always {
            archiveArtifacts(
                artifacts: 'security-evidence/correlation/**,security-evidence/selenium/**,security-evidence/suricata/**,security-evidence/security-scans/**,screenshots/**,packet-captures/scenario-b-sqli-final.pcapng',
                allowEmptyArchive: true,
                fingerprint: true
            )
        }
        success {
            echo 'Scenario B pipeline completed.'
        }
        failure {
            echo 'Scenario B pipeline failed. Review the stage logs and archived evidence.'
        }
    }
}

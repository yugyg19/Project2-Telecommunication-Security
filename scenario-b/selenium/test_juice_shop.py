import json
import os
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

BASE = Path.cwd()
EVIDENCE = BASE / "evidence" / "selenium"
SCREENSHOTS = BASE / "screenshots"
GRID = os.environ.get("SELENIUM_GRID_URL", "http://localhost:4444")
TARGET = os.environ.get("JUICE_SHOP_URL", "http://10.20.10.20:3000")

EVIDENCE.mkdir(parents=True, exist_ok=True)
SCREENSHOTS.mkdir(parents=True, exist_ok=True)

result = {
    "test": "Juice Shop Selenium browser smoke test",
    "target": TARGET,
    "started_utc": datetime.now(timezone.utc).isoformat(),
    "status": "FAIL"
}

driver = None
try:
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Remote(command_executor=GRID, options=options)
    driver.set_page_load_timeout(30)
    driver.get(TARGET)
    time.sleep(2)

    result["browser"] = driver.capabilities.get("browserName")
    result["browser_version"] = driver.capabilities.get("browserVersion")
    result["page_title"] = driver.title
    result["current_url"] = driver.current_url
    result["page_loaded"] = bool(driver.title and driver.current_url.startswith(TARGET))
    result["screenshot"] = str(SCREENSHOTS / "juice-shop-selenium.png")

    if result["page_loaded"]:
        driver.save_screenshot(result["screenshot"])
        result["status"] = "PASS"
    else:
        result["error"] = "The browser did not reach the expected target page."
except Exception as exc:
    result["error"] = f"{type(exc).__name__}: {exc}"
finally:
    if driver:
        driver.quit()
    result["finished_utc"] = datetime.now(timezone.utc).isoformat()
    output = EVIDENCE / "selenium-browser-test.json"
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    print(f"Evidence saved: {output}")

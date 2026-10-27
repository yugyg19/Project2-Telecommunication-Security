import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

TARGET = os.environ.get("JUICE_SHOP_URL", "http://10.20.10.20:3000")
GRID = os.environ.get("SELENIUM_GRID_URL", "http://scenario-b-selenium:4444")
OUT = Path.cwd() / "evidence" / "selenium"
SHOTS = Path.cwd() / "screenshots"
OUT.mkdir(parents=True, exist_ok=True)
SHOTS.mkdir(parents=True, exist_ok=True)

result = {
    "test": "Juice Shop browser authentication validation",
    "target": TARGET,
    "started_utc": datetime.now(timezone.utc).isoformat(),
    "status": "FAIL",
    "checks": {}
}
driver = None

try:
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Remote(command_executor=GRID, options=options)
    driver.set_page_load_timeout(30)
    wait = WebDriverWait(driver, 15)

    driver.get(TARGET)
    wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
    result["checks"]["home_page_loaded"] = bool(driver.title)

    # Open the login route and inspect the rendered login form.
    driver.get(TARGET + "/#/login")
    email = wait.until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR, "input[type='email'], input[name='email']")
    ))
    password = wait.until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR, "input[type='password']")
    ))
    result["checks"]["login_form_present"] = bool(email and password)

    # Dismiss the privacy/cookie consent overlay if it appears.
    for selector in [
        "button[aria-label*='dismiss' i]",
        "button[aria-label*='close' i]",
        "button[aria-label*='privacy' i]",
        ".cdk-overlay-backdrop"
    ]:
        try:
            element = driver.find_element(By.CSS_SELECTOR, selector)
            if selector == ".cdk-overlay-backdrop":
                driver.execute_script("arguments[0].click();", element)
            else:
                element.click()
            time.sleep(1)
        except Exception:
            pass

    # Do not embed credentials in the script. Supply them as environment variables.
    user = os.environ.get("JUICE_SHOP_EMAIL")
    secret = os.environ.get("JUICE_SHOP_PASSWORD")
    if not user or not secret:
        result["status"] = "BLOCKED"
        result["error"] = "Set JUICE_SHOP_EMAIL and JUICE_SHOP_PASSWORD for a real login test."
    else:
        email.clear()
        email.send_keys(user)
        password.clear()
        password.send_keys(secret)
        login_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        driver.execute_script("arguments[0].click();", login_button)

        wait.until(lambda d: "#/login" not in d.current_url)
        time.sleep(2)
        result["checks"]["login_redirected"] = "#/login" not in driver.current_url
        result["checks"]["browser_storage_nonempty"] = bool(
            driver.execute_script("return Object.keys(localStorage).length")
        )
        result["checks"]["session_cookie_names"] = [
            c["name"] for c in driver.get_cookies()
        ]
        result["authenticated_url"] = driver.current_url
        result["authenticated_screenshot"] = str(
            SHOTS / "juice-shop-authenticated.png"
        )
        driver.save_screenshot(result["authenticated_screenshot"])
        result["status"] = (
            "PASS" if all(result["checks"].get(k, False) for k in
                          ["home_page_loaded", "login_form_present", "login_redirected",
                           "browser_storage_nonempty"]) else "FAIL"
        )

except Exception as exc:
    result["error"] = f"{type(exc).__name__}: {exc}"
finally:
    if driver:
        driver.quit()
    result["finished_utc"] = datetime.now(timezone.utc).isoformat()
    (OUT / "selenium-auth-test.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    print("Evidence saved:", OUT / "selenium-auth-test.json")

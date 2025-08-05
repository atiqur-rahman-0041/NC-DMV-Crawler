from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from datetime import datetime
from dotenv import load_dotenv
from webhook import notify_discord

import os

load_dotenv()

nc_dvm_location = os.getenv('NC_DMV_LOCATION', 'Raleigh West')
discord_webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
selenium_url = os.getenv('SELENIUM_URL', 'http://localhost:4444/wd/hub')
lower_day_range = int(os.getenv('LOWER_DAY_RANGE', 0))
upper_day_range = int(os.getenv('UPPER_DAY_RANGE', 30))
appointment_type = os.getenv('APPOINTMENT_TYPE', 'Driver License - First Time')
current_year = datetime.now().year

# Set Chrome options for headless mode
options = Options()

options.add_argument('--headless=new')
options.add_argument('--window-size=1920,1080')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-blink-features=AutomationControlled')

# Start browser
driver = webdriver.Remote(
    command_executor=selenium_url,
    options=options
)
wait = WebDriverWait(driver, 10)

# Auto‐grant “geolocation” permission for the DMV origin
driver.execute_cdp_cmd(
    "Browser.grantPermissions",
    {
        "origin": "https://skiptheline.ncdot.gov",
        "permissions": ["geolocation"]
    }
)
# Spoof a real lat/lon
driver.execute_cdp_cmd(
    "Emulation.setGeolocationOverride",
    {
        "latitude": 35.7796,
        "longitude": -78.6382,
        "accuracy": 1
    }
)

try:
    driver.get("https://skiptheline.ncdot.gov/")

    # Step 1: Click "Make an Appointment"
    wait.until(EC.element_to_be_clickable((By.ID, "cmdMakeAppt"))).click()

    # Step 2: Select Appointment Type
    wait.until(EC.element_to_be_clickable((
        By.XPATH,
        f"//div[contains(text(),'{appointment_type}')]/ancestor::div[contains(@class, 'QflowObjectItem')]"
    ))).click()

    # Step 3: Click on NC DMV location if not disabled
    raleigh_xpath = (
        f"//div[contains(@class, 'QflowObjectItem') and .//div[contains(text(), '{nc_dvm_location}')]"
        " and not(contains(@class, 'disabled-unit'))]"
    )

    wait.until(EC.element_to_be_clickable((By.XPATH, raleigh_xpath))).click()

    # Step 4: Extract appointment date in either this year or next year
    date_input = wait.until(EC.presence_of_element_located((
        By.XPATH,
        f"//input[contains(@name, 'Model.Value') and @type='hidden']"
        f"[contains(@value, '{current_year}') or contains(@value, '{current_year + 1}')]"
    )))

    date_str = date_input.get_attribute("value")
    date_value = datetime.strptime(date_str, "%Y-%m-%d")

    # Step 5: Print based on proximity
    today = datetime.now()
    if lower_day_range <= (date_value - today).days <= upper_day_range:
        message = f"📍 **{nc_dvm_location} Appointment Found!**\n🗓 Date: `{date_value.date()}`"
        notify_discord(message, discord_webhook_url)
    else:
        pass
        # print(f"❌ Date is not within the next {upper_day_range} days: {date_value.date()}")
        # notify_discord(f"❌ Date is not within the next {upper_day_range} days: {date_value.date()}", discord_webhook_url)

except TimeoutException:
    print("❌ Timeout while waiting for an element.")
except Exception as e:
    print(f"❌ Script failed: {e}")
finally:
    driver.quit()

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pygetwindow as gw
import pyautogui
import re
import time

MAIL_URL = "https://webmail.eternalaccounts.net/"
CREDENTIAL_FILE_LOCATION = r"C:\Users\myrez\Documents\Accounts1.txt"

MICROBOT_TITLE = "Microbot Launcher"

WEBMAIL_USERNAME_ID = "rcmloginuser"
WEBMAIL_PASSWORD_ID = "rcmloginpwd"

def get_verification_code(email, password):
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    driver.get(MAIL_URL)

    email_box = driver.find_element(By.ID, WEBMAIL_USERNAME_ID)
    email_box.click() 
    email_box.send_keys(email)

    password_box = driver.find_element(By.ID, WEBMAIL_PASSWORD_ID)
    password_box.click()
    password_box.send_keys(password, Keys.ENTER)

    time.sleep(5)

    wait = WebDriverWait(driver, 20)

    email_text = wait.until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    ).text

    match = re.search(
    r"\b([A-Z0-9]{5})\b(?=\s+is your Jagex verification code)",
    email_text
)

    if not match:
        return ""

    verification_code = match.group(1)
    print("Verification code:", verification_code)
    driver.quit()
    return verification_code


def focus_microbot():
    windows = gw.getWindowsWithTitle(MICROBOT_TITLE)

    if not windows:
        print("Microbot Launcher not found")
        return False

    win = windows[0]

    if win.isMinimized:
        win.restore()

    win.activate()
    time.sleep(1)
    return True


def get_window_region(title_contains):
    windows = gw.getWindowsWithTitle(title_contains)
    if not windows:
        return None

    win = windows[0]
    win.activate()        # bring to foreground
    return (win.left, win.top, win.width, win.height)

def find_and_click_button(image, timeout=25, confidence=0.6, region=None):
    start = time.time()

    while time.time() - start < timeout:
        try:
            location = pyautogui.locateCenterOnScreen(
                image,
                confidence=confidence,
                region=region
            )
        except pyautogui.ImageNotFoundException:
            # Image not found this iteration, just continue
            location = None

        if location:
            pyautogui.click(location)
            print(f"Clicked {image}")
            sleep_time = 15 if "accounts" in image else 7
            time.sleep(sleep_time)
            return True

        time.sleep(0.5)

    print(f"Button not found: {image}")
    return False


def handle_credentials():
    
    updated_lines = []

    with open(CREDENTIAL_FILE_LOCATION, "r") as f:
        lines = f.readlines()

        for i, line in enumerate(lines):
            stripped = line.strip()
            verification_code = ""

            if ":" not in stripped:
                updated_lines.append(line)
                continue

            username, password = stripped.split(":", 1)

            if "completed" in password.lower():
                updated_lines.append(line)
                continue

            if not focus_microbot():
                print("Could not focus microbot launcher")
                exit

            if not find_and_click_button("assets/add_accounts_button.png", region=get_window_region(MICROBOT_TITLE)):
                print("Couldn't find the add account button.")
                exit

            if not find_and_click_button("assets/allow_cookies_button.png", timeout=10):
                print("Couldn't find the all cookies button!")
                exit
            
            if not find_and_click_button("assets/email_button_other.png", timeout=10) and not find_and_click_button("assets/email_button.png", timeout=10):
                print("Can't find the login button")
                exit
            # pyautogui.press('tab')
            # time.sleep(0.5)
            # pyautogui.press('tab')
            # time.sleep(0.5)

            pyautogui.write(username, interval=0.05)  # types each character slowly
            pyautogui.press('enter')
            time.sleep(1)
            pyautogui.write(password, interval=0.05)
            pyautogui.press('enter')
            time.sleep(1) 

            verification_code = get_verification_code(username, password)

            time.sleep(2)

            if verification_code == "":
                print("Invalid verification code.")
                exit

            time.sleep(2)

            pyautogui.write(verification_code, interval=0.05)
            pyautogui.press('enter')

            lines[i] = f"{username}:{password} - completed\n"

            with open(CREDENTIAL_FILE_LOCATION, "w") as f:
                f.writelines(lines)
            
            print(f"Completed: {username}")

            time.sleep(20)

handle_credentials()




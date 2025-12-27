from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pygetwindow as gw
import pyautogui
import time

MAIL_URL = "https://webmail.eternalaccounts.net/"
CREDENTIAL_FILE_LOCATION = r"C:\Users\myrez\Documents\Accounts1.txt"



def test_selenium(email, password):
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    driver.get(MAIL_URL)

    email_box = driver.find_element(By.NAME, "email")  # or ID
    email_box.click()          # focus
    email_box.send_keys(email)

    password_box = driver.find_element(By.NAME, "password")
    password_box.click()
    password_box.send_keys(password, Keys.ENTER)


def focus_microbot():
    windows = gw.getWindowsWithTitle("Microbot Launcher")

    if not windows:
        print("Microbot Launcher not found")
        return False

    win = windows[0]

    if win.isMinimized:
        win.restore()

    win.activate()
    time.sleep(0.5)  # allow focus to settle
    return True


def find_and_click_button(image, timeout=10, confidence=0.8):
    start = time.time()

    while time.time() - start < timeout:
        location = pyautogui.locateCenterOnScreen(
            image,
            confidence=confidence
        )

        if location:
            pyautogui.click(location)
            print(f"Clicked {image}")
            time.sleep(5)
            return True

        time.sleep(0.5)

    print(f"Button not found: {image}")
    return False



def handle_credentials():
    updated_lines = []

    with open(CREDENTIAL_FILE_LOCATION, "r") as f:
        for line in f:
            stripped = line.strip()

            if ":" not in stripped:
                updated_lines.append(line)
                continue

            username, password = stripped.split(":", 1)

            if "completed" in password.lower():
                updated_lines.append(line)
                continue

            # Find button on microbot launcher


            print(username)
            print(password)
            print("-------")

            updated_lines.append(f"{username}:{password} - completed\n")

    # with open(CREDENTIAL_FILE_LOCATION, "w") as f:
    #     f.writelines(updated_lines)

# handle_credentials()

# if not focus_microbot():
#     print("Could not focus microbot launcher")
#     exit

# if not find_and_click_button("assets/add_accounts_button.png"):
#     print("Couldn't find the add account button.")
#     exit

# if not find_and_click_button("assets/allow_cookies_button.png"):
#     print("Couldn't find the all cookies button!")
#     exit

test_selenium("test", "Test")


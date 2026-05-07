from selenium import webdriver
from selenium.common.exceptions import UnexpectedAlertPresentException, NoAlertPresentException, WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver
import time
from bs4 import BeautifulSoup
from config import WAIT_SEC_FETCH_HTML

def make_driver():
    options = Options()
    options.add_argument("--start-maximized")
    return webdriver.Chrome(options=options)

def _accept_alert(driver: WebDriver):
    try:
        alert = driver.switch_to.alert
        print(f"[Alert] detected: {alert.text}")
        alert.accept()
    except NoAlertPresentException:
        pass
    except Exception as e:
        print(f"[Alert] accept failed: {e}")

def fetch_html(driver: WebDriver, url: str, wait_sec: int = 5):
    try:
        driver.get(url)
    except UnexpectedAlertPresentException as e:
        print(f"Unexpected alert on GET {url}: {e}")
        _accept_alert(driver)
        time.sleep(1)
        try:
            driver.get(url)
        except Exception as second_e:
            print(f"Retry failed after accepting alert: {second_e}")
            return None
    except WebDriverException as e:
        print(f"WebDriver error on GET {url}: {e}")
        return None

    time.sleep(wait_sec)
    return driver.page_source

def make_soup(html: str) -> BeautifulSoup:
    soup = BeautifulSoup(html, "html.parser")
    return soup
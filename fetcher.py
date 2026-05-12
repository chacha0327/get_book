from selenium import webdriver
from selenium.common.exceptions import UnexpectedAlertPresentException, NoAlertPresentException, WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver
import time
from bs4 import BeautifulSoup
from config import WAIT_SEC_FETCH_HTML
from log import log_error, log_info
from storage import save_error_url

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
        time.sleep(wait_sec)
        return driver.page_source
    except UnexpectedAlertPresentException as e:
        log_error(f"Unexpected alert on GET {url}: {e}")
        save_error_url(url)
        _accept_alert(driver)
        time.sleep(1)
        try:
            driver.get(url)
        except Exception as second_e:
            log_error(f"Retry failed after accepting alert: {second_e}")
            return None
    except WebDriverException as e:
        log_error(f"WebDriver error on GET {url}: {e}")
        save_error_url(url)
        return None
    except TypeError as third_e:
        log_error(f"Type error on GET {url}: {third_e}")
        save_error_url(url)
        return None


def make_soup(html: str) -> BeautifulSoup:
    soup = BeautifulSoup(html, "html.parser")
    return soup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup

def make_driver():
    options = Options()
    options.add_argument("--start-maximized")
    return webdriver.Chrome(options=options)

def fetch_html(driver: Options, url: str, wait_sec: int = 5):
    driver.get(url)
    time.sleep(wait_sec)
    return driver.page_source

def make_soup(html: str) -> BeautifulSoup:
    soup = BeautifulSoup(html, "html.parser")
    return soup
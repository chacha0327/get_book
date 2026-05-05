from config import BASE_URL, UA, max_page, max_book, CARD_FILE
from fetcher import make_driver, fetch_html, make_soup
from models import Bookdetail
from parser import extract_isbn, extract_name, get_comment_url_and_product_id, crawel_product, get_details
from storage import save_jsonl_file, convert_json
from utils import save_debug_file, time_clock
from typing import Dict, List
import re, time, random
from selenium.webdriver.chrome.options import Options
from check import check_card, check_seen_ids
from card import get_card

def loop_page(card_url, max_page: int, max_book: int):
    seen = set()
    for n in range(1, max_page+1):
        driver = make_driver()
        print(f"page [{n}/{max_page}]") 
        url = f"{card_url}page={n}"
        html = fetch_html(driver=driver, url=url)
        soup = make_soup(html)
        product_url = crawel_product(soup)
        driver.quit()
        for idx, url in enumerate(product_url[:max_book], start=1):
            print(f"book: [{idx}/{len(product_url)}]")
            detail = get_details(url)
            if detail:
                save_jsonl_file(detail)
            time.sleep(random.uniform(10, 20))
            time_clock(idx, 20, 60.0)
        print("this page is OK")
        convert_json()

def run():
    cards = check_card()
    for idx, card in enumerate(cards[:2], start=1):
        card_url = card["url"]
        print(card_url)
        print(f"[{card["text"]}]")
        loop_page(card_url, max_page, max_book)
        time.sleep(random.uniform(5, 10))
        time_clock(idx, 20, 30.0)
    print("end")
        


if __name__ == "__main__":
    run()
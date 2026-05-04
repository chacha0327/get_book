from config import BASE_URL, UA, max_page, max_book, CARD_FILE
from fetcher import make_driver, fetch_html, make_soup
from models import Bookdetail
from parser import extract_isbn, extract_name, get_comment_url_and_product_id, crawel_product, get_details, get_card
from storage import save_jsonl_file, convert_json, save_cards, loads_cards_id, loads_cards
from utils import save_debug_file, time_clock
from typing import Dict, List
import re, time, random
from selenium.webdriver.chrome.options import Options
from check import check_card

def get_card() -> List[Dict]:
    driver = make_driver()
    try:
        out = []
        html = fetch_html(driver=driver, url=BASE_URL)
        soup = make_soup(html)
        items = soup.find_all("li")
        if items:
            for item in items:
                id_tag = item.find("input", {"id": re.compile(r"check-sub-[a-z0-9]+-\d+")})
                if id_tag:
                    id_ = id_tag.get("id")
                    name = id_tag.get("name")
                    value = id_tag.get("value")
                    label = item.find("label", {"for": id_})
                    span_text = label.get_text(strip=True)
                    match_ = re.match(r"(.*)\((\d+)\)", span_text)
                    count = match_.group(2)
                    text = match_.group(1)
                    if text != "全部":
                        out.append({
                            "text": text,
                            "name": name,
                            "value": value,
                            "id": id_,
                            "url": f"https://www.books.com.tw/booksComment/filterComment/{name}?sub={value}&star=all&release=all&touch=all&cvt=all&forsale=&sort=1&"
                        })               
    finally:
        print("get card OK")
        print(out)
        driver.quit()
        return out
def loop_page(card_url, max_page: int, max_book: int):
    seen = set()
    for n in range(1, max_page+1):
        try:
            driver = make_driver()
            print(f"page [{n}/{max_page}]") 
            url = f"{card_url}page={n}"
            html = fetch_html(driver=driver, url=url)
            soup = make_soup(html)
            product_url = crawel_product(soup)
            for idx, url in enumerate(product_url[:max_book], start=1):
                print(f"book: [{idx}/{len(product_url)}]")
                detail = get_details(url)
                if detail:
                    save_jsonl_file(detail)
                time.sleep(random.uniform(10, 20))
                time_clock(idx, 20, 60.0)
        finally:
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

from fetcher import make_driver, fetch_html, make_soup
from parser import crawel_product, get_details
from storage import save_jsonl_file, convert_json
from utils import time_clock
import time, random
from check import check_card
from log import log_info, log_error
import keyboard


def loop_page(card_url, max_page: int, max_book: int):
    seen = set()
    for n in range(1, max_page+1):
        driver = make_driver()
        log_info(f"page [{n}/{max_page}]")
        url = f"{card_url}page={n}"
        html = fetch_html(driver=driver, url=url)
        soup = make_soup(html)
        product_url = crawel_product(soup)
        driver.quit()
        for idx, url in enumerate(product_url[:max_book], start=1):
            log_info(f"book: [{idx}/{len(product_url)}]")
            detail = get_details(url)
            if detail:
                save_jsonl_file(detail)
            time.sleep(random.uniform(10, 20))
            time_clock(idx, 20, 60.0)
        log_info(f"Page[{n}] OK!")
        convert_json()

def setting():
    setting = list(input("maxpage maxbook").split(" "))
    return int(setting[0]), int(setting[1])


def run():
    max_page, max_book = setting()
    cards = check_card()
    for idx, card in enumerate(cards, start=1):
        card_url = card["url"]
        log_info(f"[{card["text"]}]")
        loop_page(card_url, max_page, max_book)
        time.sleep(random.uniform(5, 10))
        time_clock(idx, 20, 30.0)
    print("end")
        


if __name__ == "__main__":
    convert_json()
    run()
from fetcher import make_driver, fetch_html, make_soup
from typing import List, Dict
import re, json
from config import CARD_FILE, BASE_URL, JSONL_FILE
def get_card() -> List[Dict]:
    driver = make_driver()
    try:
        out = []
        html = fetch_html(driver, BASE_URL)
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
        save_cards(out)
        driver.quit()
        return out
def save_cards(cards):
    with open(CARD_FILE, "w", encoding="utf-8") as f:
        json.dump(cards, f, ensure_ascii=False, indent=2)

def loads_cards_id() -> set[str]:
    if not CARD_FILE.exists():
        return set()
    with open(CARD_FILE, "r", encoding="utf-8") as f:
        return {card["id"].strip() for card in f if card["id"].strip()}
def loads_cards():
    with open(CARD_FILE, "r", encoding="utf-8") as f:
        return [card.strip() for card in f if card.strip()]

def loads_cards_url() :
    if not JSONL_FILE.exists():
        return set()
    with open(JSONL_FILE, "r", encoding="utf-8") as f:
        return {json.loads(line).get("product_url") for line in f if line.strip()}
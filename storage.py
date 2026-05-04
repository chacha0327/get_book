from dataclasses import asdict
import json
from config import DATA_DIR, JSONL_FILE, SEEN_FILE, FAIL_FILE, JSON_FILE, CARD_FILE
from models import Bookdetail
def save_jsonl_file(detail):

    with open(JSONL_FILE, "a", encoding="utf-8") as f:
        json.dump(asdict(detail), f, ensure_ascii=False)
        f.write("\n")

def convert_json():
    data = []
    with open(JSONL_FILE, "r", encoding="utf-8") as f:
        for line in f:
            data.append(json.loads(line))
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2) 

def load_seen_ids() -> set[str]:
    if not SEEN_FILE.exists():
        return set()

    with open(SEEN_FILE, "r", encoding="utf-8") as f:
        return {line.strip() for line in f if line.strip()}


def save_seen_id(product_id: str):
    with open(SEEN_FILE, "a", encoding="utf-8") as f:
        f.write(product_id + "\n")


def save_failed_url(url: str):
    with open(FAIL_FILE, "a", encoding="utf-8") as f:
        f.write(url + "\n")

def check_seen_ids(obj_):
    seen = load_seen_ids()
    if obj_ not in seen:
        save_seen_id(obj_)
        print(f"{obj_} saved")
        return True
    print("in seen")
    return False
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


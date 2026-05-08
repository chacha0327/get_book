from card import get_card
from config import CARD_FILE
from storage import load_seen_ids, save_seen_id, load_error_url, save_error_url
import json
def check_card():
    if not CARD_FILE.exists():
        print("skip")
        return get_card()
    print("card had been saved")
    with open(CARD_FILE, "r", encoding="utf-8") as f:
        return json.load(f)
def check_seen_ids(obj_):
    seen = load_seen_ids()
    if obj_ not in seen:
        save_seen_id(obj_)
        print(f"{obj_} saved")
        return True
    print("check card return False Please find the reason")
    return False
def check_error_url(url):
    seen_url = load_error_url()
    if url not in seen_url():
        save_error_url(url)
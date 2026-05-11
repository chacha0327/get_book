from card import get_card
from config import CARD_FILE
from storage import load_seen_ids, save_seen_id, load_error_url, save_error_url
import json
from log import log_error, log_info
def check_card():
    if not CARD_FILE.exists():
        log_info("skip getting card")
        return get_card()
    log_info("card had been saved")
    with open(CARD_FILE, "r", encoding="utf-8") as f:
        return json.load(f)
def check_seen_ids(obj_, error=True):
    seen = load_seen_ids()
    if obj_ not in seen and error:
        save_seen_id(obj_)
        log_info(f"{obj_} saved")
        return True
    log_error("check card return False Please find the reason")
    return None
def check_error_url(url):
    seen_url = load_error_url()
    if url not in seen_url():
        save_error_url(url)
from parser import get_card
from config import CARD_FILE
import json
def check_card():
    if not CARD_FILE.exists():
        print("skip")
        return get_card()
    print("card had been saved")
    with open(CARD_FILE, "r", encoding="utf-8") as f:
        return json.load(f)
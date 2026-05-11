from pathlib import Path
from loguru import logger
BASE_URL = "https://www.books.com.tw/booksComment/filterComment/"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36"
max_page = 10
max_book = 50
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
JSONL_FILE = DATA_DIR / "books.jsonl"
SEEN_FILE = DATA_DIR / "seen_ids.txt"
FAIL_FILE = DATA_DIR / "failed_urls.txt"
JSON_FILE = DATA_DIR / "books.json"
CARD_FILE = DATA_DIR / "seen_cards.json"
ERROR_URL = DATA_DIR / "error_url.txt"
WAIT_SEC_FETCH_HTML = 5


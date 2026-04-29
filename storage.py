from dataclasses import asdict
import json
from config import DATA_DIR, JSONL_FILE, SEEN_FILE, FAIL_FILE

def save_jsonl_file(detail, filename: str):

    with open(f"{filename}.jsonl", "a", encoding="utf-8") as f:
        json.dump(asdict(detail), f, ensure_ascii=False)
        f.write("\n")

def convert_json(filename_1: str, filename_2: str):
    data = []
    with open(filename_1, "r", encoding="utf-8") as f:
        for line in f:
            data.append(json.loads(line))
    with open(filename_2, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2) 

def load_seen_ids() -> set[str]:
    if not SEEN_FILE.exists():
        return set()

    with open(SEEN_FILE, "r", encoding="utf-8") as f:
        return {line.strip() for line in f if line.strip()}


def save_seen_id(product_id: str):
    with open(SEEN_FILE, "a", encoding="utf-8") as f:
        f.write(product_id + "\n")
import time

def save_debug_file(error, content):
    with open(f"{error}.html", "w", encoding="utf-8") as f:
        f.write(content)

def time_clock(idx, frequency: int, second: float):
    if idx % frequency == 0:
        time.sleep(second)




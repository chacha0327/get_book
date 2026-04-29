
def save_debug_file(error, content):
    with open(f"{error}.html", "w", encoding="utf-8") as f:
        f.write(content)


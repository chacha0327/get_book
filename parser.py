from bs4 import BeautifulSoup
from typing import Optional, List, Tuple
from urllib.parse import urlparse
import re
from utils import save_debug_file
from models import Bookdetail
from selenium.webdriver.chrome import options
from fetcher import fetch_html, make_soup
def extract_isbn(soup: BeautifulSoup)  -> Optional[List]:
    text = soup.get_text(" ", strip=True)
    m = re.search(r"ISBN[：:]\s*(\d+)", text)
    return m.group(1) if m else None
def extract_name(soup: BeautifulSoup) -> Optional[List]:
    meta = soup.find("meta", property="og:title")
    if meta:
        name = meta.get("content")
        return name
    t = soup.find("title")
    return t.get_text(strip=True) if t else None
def get_comment_url_and_product_id(product_url):
    parsed = urlparse(product_url)
    product_id = parsed.path.split("/")[-1]
    comment_url = f"https://www.books.com.tw/booksComment/getCommemt/{product_id}"
    return product_id, comment_url
def crawel_product(soup: BeautifulSoup) -> List[str]:
    out = []
    seen = set()
    try:
        h1 = soup.find_all("h1")
        if h1:
            for a in h1:
                href = a.find("a", href=re.compile(r"https://www\.books\.com\.tw/products/[A-Za-z0-9]"))
                url = href.get("href")
                if href and href not in seen:
                    url = href.get("href")
                    out.append(url)
            return out
    except AttributeError as e:
        save_debug_file("crawel_book", soup.text)
        print(e)

def get_details(product_url: str, driver: options) -> Bookdetail:
    prodcut_id, comment_url = get_comment_url_and_product_id(product_url)
    s = fetch_html(driver=driver, url=product_url)
    if not s:
        return Bookdetail(
            name=None,
            isbn=None,
            comment_url=comment_url,
            product_url=product_url,
            product_id=prodcut_id           
        )
    if s:
        soup = make_soup(s)
        name = extract_name(soup)
        isbn = extract_isbn(soup)
        synopsis = get_synopsis(soup)
        print(f"OK: name: {name}")
        return Bookdetail(
            name=name,
            isbn=isbn,
            comment_url=comment_url,
            product_url=product_url,
            product_id=prodcut_id,
            synopsis=synopsis
        )

def get_synopsis(soup: BeautifulSoup):
    contents = soup.find_all("div", {"class": "content"}, {"style": "height:auto;"})
    t = ""
    for c in contents[:2]:
        text = c.get_text(separator="\n", strip=True)
        t += text
    return t
        
from dataclasses import dataclass
from typing import Optional

@dataclass
class Bookdetail:
    name: Optional[str]
    isbn: Optional[str]
    comment_url: str
    product_url: str
    product_id: str
    synopsis: str
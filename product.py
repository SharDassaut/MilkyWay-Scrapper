from dataclasses import dataclass, asdict

@dataclass
class Product:
    title: str
    volume: str
    authors: list
    price: str
    cover_url: str
    tags: list
    original_title: str
    format: str
    size: str
    page_number: str
    color: str
    isbn: str

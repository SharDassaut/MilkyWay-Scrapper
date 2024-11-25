#This file is part of the "MilkyWay Ediciones Scraper" project.
from dataclasses import dataclass, asdict

@dataclass
class Product:
    title: str | None
    volume: str | None
    authors: list | None
    price: str | None
    cover_url: str | None
    tags: list | None
    original_title: str | None
    format: str | None
    size: str | None
    page_number: str | None
    color: str | None
    isbn: str | None

    def toDict(self):
        asdict(self)
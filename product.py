#This file is part of the "MilkyWay Ediciones Scraper" project.
from dataclasses import dataclass, field

@dataclass
class Product:
    title: str = field(default_factory=None)
    volume: str = field(default_factory=None)
    authors: list = field(default_factory=None)
    price: str = field(default_factory=None)
    cover_url: str = field(default_factory=None)
    tags: list = field(default_factory=None)
    booktrailer: str = field(default_factory=None)
    original_title: str = field(default_factory=None)
    format: str = field(default_factory=None)
    size: str = field(default_factory=None)
    page_number: str= field(default_factory=None)
    color: str = field(default_factory=None)
    isbn: str = field(default_factory=None)


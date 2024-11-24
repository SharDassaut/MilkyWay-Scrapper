class Product:
    def __init__(self, title, volume, author,price, coverUrl):
        self.title = title
        self.volume = volume
        self.author = author
        self.price = price
        self.coverUrl = coverUrl

    def __str__(self):
        return f"{self.title} {self.volume}"

    def to_dict(self):
        return {
            "title": self.title,
            "volume":self.volume,
            "author":self.author,
            "price": self.price,
            "coverUrl": self.coverUrl
        }
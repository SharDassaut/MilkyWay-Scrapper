class Product:
    def __init__(self, titulo, precio, urlPortada):
        self.titulo = titulo
        self.precio = precio
        self.urlPortada = urlPortada

    def __str__(self):
        return f"{self.titulo} costs {self.precio}"

    def to_dict(self):
        return {
            "titulo": self.titulo,
            "precio": self.precio,
            "urlPortada": self.urlPortada
        }
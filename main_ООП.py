from itertools import product
from unicodedata import category


class Product:
    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity


class Category:
    total_categories = 0
    total_product = 0

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.products = []  # список товаров категории

        Category.total_categories += 1
        Category.total_product += len(product)

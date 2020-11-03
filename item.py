class Item:
    TYPES = ("sword", "bow", "spell")

    def __init__(self, price, weight, type):
        self.price = price
        self.weight = weight
        self.type = type


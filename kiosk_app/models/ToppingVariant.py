class Topping:
    def __init__(self, id: int, name: str, price: int, discountPrice: int):
        self.id = id
        self.name = name
        self.price = price
        self.discountPrice = discountPrice
        self.discount = self.price - self.discountPrice

    def __eq__(self, other):
        if isinstance(other, Topping):
            return self.id == other.id


class Variant:
    def __init__(self, id: int, value: str, price: int = 0, additional_cost: int = 0):
        self.id = id
        self.value = value
        self.price = price
        self.additional_cost = additional_cost

    def __eq__(self, other):
        if isinstance(other, Variant):
            return self.id == other.id
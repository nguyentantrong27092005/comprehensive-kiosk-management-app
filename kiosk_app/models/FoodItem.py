class FoodItem:
    def __init__(self, id: int, name: str, price: int, discounted_price: int, image_url: str, is_best_seller: bool, promotion_id = None):
        self.id = id
        self.name = name
        self.price = price
        self.image_url = image_url
        self.is_best_seller = is_best_seller
        self.discounted_price = discounted_price
        self.promotion_id = promotion_id
        self.discount = self.price - self.discounted_price

    def __repr__(self):
        return (f'{self.__class__.__name__}'
                f'(id={self.id!r}, name={self.name!r}), price={self.price!r}')

    def __eq__(self, other):
        if isinstance(other, FoodItem):
            return self.id == other.id and self.promotion_id == other.promotion_id
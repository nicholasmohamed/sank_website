class ShoppingCart:

    def __init__(self):
        self.items = []

    # add an item to the cart
    def add_to_cart(self, item_id, quantity):
        # if item already exists in cart, do nothing
        for item in self.items:
            if item['id'] == item_id:
                return

        self.items.append({'id': item_id, 'quantity': quantity})

    # remove an item from the cart
    def remove_from_cart(self, item_id):
        # find existing item and remove it
        for item in self.items:
            if item['id'] == item_id:
                self.items.remove(item)

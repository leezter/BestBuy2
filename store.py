class Store:
    """ A class representing a store that holds and manages multiple Product instances."""


    def __init__(self, products):
        """ Initialise the store with a list of products. """
        self.products = products
    
        
    def add_product(self, product):
        """ Adds a new product to the store. """
        self.products.append(product)
        

    def remove_product(self, product):
        """ Removes a product from the store if it exists. """
        if product in self.products:
            self.products.remove(product)


    def get_total_quantity(self):
        """ Returns the total quantity of all products in the store """
        total = 0
        for product in self.products:
            total += product.get_quantity()
        return total


    def get_all_products(self):
        """ Returns a list of all active products in the store """
        active_products = []
        for product in self.products:
            if product.is_active():
                active_products.append(product)
        return active_products


    def order(self, shopping_list):
        """ Processes an order based on a list of (product, quantity) tuples.
            Returns the total price of the entire order. """
        total_price = 0
        for item in shopping_list:
            product = item[0]
            quantity = item[1]
            total_price += product.buy(quantity)
        return total_price
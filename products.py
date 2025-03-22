class Product:
    def __init__(self, name, price, quantity):
        """ Initiator (constructor) method. 
            Creates the instance variables. 
            If something is invalid (empty name / negative price or quantity), raises an exception. """
        if not name or price < 0 or quantity < 0:
            raise Exception("Error with your choice! Try again!")
        self.name = name
        self.price = price
        self.quantity = quantity
        self.active = True


    def get_quantity(self) -> int:
        """ Getter function for quantity.Returns the quantity (int). """
        return self.quantity


    def set_quantity(self, quantity):
        """ Setter function for quantity. If quantity reaches 0, deactivates the product. """
        self.quantity = quantity
        if self.quantity == 0:
            self.deactivate()

    def is_active(self) -> bool:
        """ Getter function for active. Returns True if the product is active, otherwise False. """
        return self.active

    def activate(self):
        """ Activates the product. """
        self.active = True

    def deactivate(self):
        """ Deactivates the product. """
        self.active = False


    def show(self) -> str:
        """ Returns a string that represents the product. """
        return f"{self.name}, Price: {self.price}, Quantity: {self.quantity}" 


    def buy(self, quantity) -> float:
        """ Buys a given quantity of the product.
        Returns the total price of the purchase.
        Updates the quantity of the product.
        In case of a problem, raises an Exception. """
        if not self.active:
            raise Exception("Product not active")
        if quantity > self.quantity:
            raise Exception("Not enough stock available.")
        if quantity <= 0:
            raise Exception("Quantity must be greater than 0")
        self.quantity -= quantity
        if self.quantity == 0:
            self.deactivate()
        return self.price * quantity
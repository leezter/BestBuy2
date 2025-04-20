from abc import ABC, abstractmethod

class Product:
    """Represents a product with a name, price, quantity, and active status."""


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
        self.promotion = None


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


    def get_promotion(self):
        """ Getter for promotion. """
        return self.promotion


    def set_promotion(self, promotion):
        """ Setter for promotion. """
        self.promotion = promotion


    def show(self) -> str:
        """ Returns a string that represents the product. """
        promotion_info = f", Promotion: {self.promotion.name}" if self.promotion else ", Promotion: None"
        return f"{self.name}, Price: ${self.price}, Quantity: {self.quantity}{promotion_info}"


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
        
        # Calculate price with promotion if exists
        if self.promotion:
            total_price = self.promotion.apply_promotion(self, quantity)
        else:
            total_price = self.price * quantity
        
        self.quantity -= quantity
        if self.quantity == 0:
            self.deactivate()
        return total_price


class NonStockedProduct(Product):
    """Represents a product that doesn't have physical stock (e.g., software licenses)."""
    
    def __init__(self, name, price):
        """Initialize a non-stocked product with quantity always set to 0."""
        super().__init__(name, price, quantity=0)
    
    def set_quantity(self, quantity):
        """Override to prevent quantity changes."""
        pass
    
    def buy(self, quantity) -> float:
        """Override to allow purchase without quantity checks."""
        if not self.active:
            raise Exception("Product not active")
        if quantity <= 0:
            raise Exception("Quantity must be greater than 0")
        
        # Calculate price with promotion if exists
        if self.promotion:
            return self.promotion.apply_promotion(self, quantity)
        return self.price * quantity
    
    def show(self) -> str:
        """Override to show that this is a digital product."""
        promotion_info = f", Promotion: {self.promotion.name}" if self.promotion else ", Promotion: None"
        return f"{self.name}, Price: ${self.price}, Quantity: Unlimited{promotion_info}"


class LimitedProduct(Product):
    """Represents a product that can only be purchased a limited number of times per order."""
    
    def __init__(self, name, price, quantity, maximum):
        """Initialize a limited product with a maximum purchase quantity per order."""
        super().__init__(name, price, quantity)
        self.maximum = maximum
    
    def buy(self, quantity) -> float:
        """Override to enforce maximum purchase limit."""
        if quantity > self.maximum:
            raise Exception(f"Cannot purchase more than {self.maximum} of this product in a single order")
        
        # Calculate price with promotion if exists
        if self.promotion:
            total_price = self.promotion.apply_promotion(self, quantity)
        else:
            total_price = super().buy(quantity)
        
        return total_price
    
    def show(self) -> str:
        """Override to show the maximum purchase limit."""
        promotion_info = f", Promotion: {self.promotion.name}" if self.promotion else ", Promotion: None"
        return f"{self.name}, Price: ${self.price}, Limited to {self.maximum} per order!{promotion_info}"


class Promotion(ABC):
    """Abstract base class for promotions."""
    
    def __init__(self, name):
        self.name = name
    
    @abstractmethod
    def apply_promotion(self, product, quantity) -> float:
        """Apply the promotion to the product and return the discounted price."""
        pass


class PercentageDiscount(Promotion):
    """Promotion that applies a percentage discount."""
    
    def __init__(self, name, percentage):
        super().__init__(name)
        self.percentage = percentage
    
    def apply_promotion(self, product, quantity) -> float:
        """Apply percentage discount to the total price."""
        total_price = product.price * quantity
        discount = total_price * (self.percentage / 100)
        return total_price - discount


class SecondHalfPrice(Promotion):
    """Promotion that gives the second item at half price."""
    
    def __init__(self, name):
        super().__init__(name)
    
    def apply_promotion(self, product, quantity) -> float:
        """Calculate price with every second item at half price."""
        pairs = quantity // 2
        remainder = quantity % 2
        return (pairs * (product.price + product.price * 0.5)) + (remainder * product.price)


class Buy2Get1Free(Promotion):
    """Promotion that gives one free item for every two purchased."""
    
    def __init__(self, name):
        super().__init__(name)
    
    def apply_promotion(self, product, quantity) -> float:
        """Calculate price with every third item free."""
        groups_of_three = quantity // 3
        remainder = quantity % 3
        return (groups_of_three * 2 * product.price) + (remainder * product.price)
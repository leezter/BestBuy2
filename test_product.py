import pytest
from products import Product, NonStockedProduct, LimitedProduct, Promotion, PercentageDiscount, SecondHalfPrice, Buy2Get1Free
from store import Store

def test_create_normal_product():
    """Test that creating a normal product works."""
    product = Product("MacBook Air M2", price=1450, quantity=100)
    assert product.name == "MacBook Air M2"
    assert product.price == 1450
    assert product.quantity == 100
    assert product.is_active() is True

def test_create_product_invalid_details():
    """Test that creating a product with invalid details raises an exception."""
    # Test empty name
    with pytest.raises(Exception):
        Product("", price=1450, quantity=100)
    
    # Test negative price
    with pytest.raises(Exception):
        Product("MacBook Air M2", price=-10, quantity=100)
    
    # Test negative quantity
    with pytest.raises(Exception):
        Product("MacBook Air M2", price=1450, quantity=-100)

def test_product_becomes_inactive():
    """Test that when a product reaches 0 quantity, it becomes inactive."""
    product = Product("MacBook Air M2", price=1450, quantity=1)
    assert product.is_active() is True
    
    # Buy the last item
    product.buy(1)
    assert product.quantity == 0
    assert product.is_active() is False

def test_product_purchase():
    """Test that product purchase modifies the quantity and returns the right output."""
    product = Product("MacBook Air M2", price=1450, quantity=100)
    
    # Buy 2 items
    total_price = product.buy(2)
    
    assert product.quantity == 98
    assert total_price == 2900  # 2 * 1450

def test_buy_larger_quantity():
    """Test that buying a larger quantity than exists raises an exception."""
    product = Product("MacBook Air M2", price=1450, quantity=100)
    
    with pytest.raises(Exception):
        product.buy(101)  # Try to buy more than available

def test_non_stocked_product():
    """Test non-stocked product behavior."""
    digital = NonStockedProduct("Windows License", price=125)
    assert digital.quantity == 0
    assert "Quantity: Unlimited" in digital.show()
    
    # Should be able to buy any quantity
    total = digital.buy(5)
    assert total == 625
    assert digital.quantity == 0

def test_limited_product():
    """Test limited product behavior."""
    limited = LimitedProduct("Shipping", price=10, quantity=250, maximum=1)
    assert "Limited to 1 per order!" in limited.show()
    
    # Should be able to buy within limit
    total = limited.buy(1)
    assert total == 10
    assert limited.quantity == 249
    
    # Should not be able to buy more than maximum
    with pytest.raises(Exception):
        limited.buy(2)

def test_store_with_all_products():
    """Test store initialization with all product types."""
    product_list = [
        Product("MacBook Air M2", price=1450, quantity=100),
        Product("Bose QuietComfort Earbuds", price=250, quantity=500),
        Product("Google Pixel 7", price=500, quantity=250),
        NonStockedProduct("Windows License", price=125),
        LimitedProduct("Shipping", price=10, quantity=250, maximum=1)
    ]
    
    store = Store(product_list)
    assert len(store.products) == 5

def test_promotions():
    """Test all promotion types."""
    # Create products
    product_list = [
        Product("MacBook Air M2", price=1450, quantity=100),
        Product("Bose QuietComfort Earbuds", price=250, quantity=500),
        Product("Google Pixel 7", price=500, quantity=250),
        NonStockedProduct("Windows License", price=125),
        LimitedProduct("Shipping", price=10, quantity=250, maximum=1)
    ]

    # Create promotions
    second_half_price = SecondHalfPrice("Second Half price!")
    third_one_free = Buy2Get1Free("Third One Free!")
    thirty_percent = PercentageDiscount("30% off!", 30)

    # Test second half price promotion
    product_list[0].set_promotion(second_half_price)
    assert product_list[0].get_promotion().name == "Second Half price!"
    # Buy 2 items: 1450 + 725 = 2175
    assert product_list[0].buy(2) == 2175
    # Buy 3 items: 1450 + 725 + 1450 = 3625
    assert product_list[0].buy(3) == 3625

    # Test buy 2 get 1 free promotion
    product_list[1].set_promotion(third_one_free)
    assert product_list[1].get_promotion().name == "Third One Free!"
    # Buy 3 items: pay for 2 = 500
    assert product_list[1].buy(3) == 500
    # Buy 4 items: pay for 3 = 750
    assert product_list[1].buy(4) == 750

    # Test percentage discount promotion
    product_list[3].set_promotion(thirty_percent)
    assert product_list[3].get_promotion().name == "30% off!"
    # Buy 2 items with 30% off: 250 * 0.7 = 175
    assert product_list[3].buy(2) == 175

    # Test promotion display in show method
    assert "Promotion: Second Half price!" in product_list[0].show()
    assert "Promotion: Third One Free!" in product_list[1].show()
    assert "Promotion: 30% off!" in product_list[3].show()

def test_promotion_removal():
    """Test removing promotions from products."""
    product = Product("MacBook Air M2", price=1450, quantity=100)
    promotion = PercentageDiscount("20% off", 20)
    
    # Add promotion
    product.set_promotion(promotion)
    assert product.get_promotion() is not None
    
    # Remove promotion
    product.set_promotion(None)
    assert product.get_promotion() is None
    
    # Verify price calculation without promotion
    assert product.buy(2) == 2900  # 2 * 1450 
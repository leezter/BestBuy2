import pytest
from products import Product, NonStockedProduct, LimitedProduct
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
    assert "(Digital Product)" in digital.show()
    
    # Should be able to buy any quantity
    total = digital.buy(5)
    assert total == 625
    assert digital.quantity == 0

def test_limited_product():
    """Test limited product behavior."""
    limited = LimitedProduct("Shipping", price=10, quantity=250, maximum=1)
    assert "(Maximum per order: 1)" in limited.show()
    
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
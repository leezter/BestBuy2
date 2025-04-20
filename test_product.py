import pytest
from products import Product

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
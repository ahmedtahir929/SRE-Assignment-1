"""Refactored order calculator for the SREE practical.
Maintains original public interfaces, discount rates, and delivery charges (in PKR).
"""

from typing import List, Dict, Any

# Named constants replacing magic numbers
STUDENT_DISCOUNT_RATE = 0.10
STAFF_DISCOUNT_RATE = 0.05
REGULAR_DISCOUNT_RATE = 0.0

EXPRESS_DELIVERY_FEE = 250
STANDARD_DELIVERY_FEE = 100
DEFAULT_DELIVERY_FEE = 0


def validate_items(items: List[Dict[str, Any]]) -> None:
    """Validate that item prices and quantities are non-negative."""
    for item in items:
        if item.get('price', 0) < 0 or item.get('qty', 0) < 0:
            raise ValueError(f"Invalid negative price or quantity in item: {item.get('name', 'Unknown')}")


def calculate_subtotal(items: List[Dict[str, Any]]) -> float:
    """Calculate the raw subtotal across all items regardless of category."""
    validate_items(items)
    return sum(item['price'] * item['qty'] for item in items)


def calculate_discount(subtotal: float, customer_type: str) -> float:
    """Calculate the discount amount based on customer eligibility."""
    discount_rates = {
        'student': STUDENT_DISCOUNT_RATE,
        'staff': STAFF_DISCOUNT_RATE,
    }
    rate = discount_rates.get(customer_type, REGULAR_DISCOUNT_RATE)
    return subtotal * rate


def calculate_delivery_fee(delivery_method: str) -> int:
    """Return the applicable delivery fee for the chosen delivery method."""
    delivery_fees = {
        'express': EXPRESS_DELIVERY_FEE,
        'standard': STANDARD_DELIVERY_FEE,
    }
    return delivery_fees.get(delivery_method, DEFAULT_DELIVERY_FEE)


def order_total(items: List[Dict[str, Any]], customer_type: str, delivery: str) -> float:
    """Calculate the final rounded order total after discounts and delivery fees."""
    subtotal = calculate_subtotal(items)
    discount = calculate_discount(subtotal, customer_type)
    delivery_fee = calculate_delivery_fee(delivery)
    
    final_total = (subtotal - discount) + delivery_fee
    return round(final_total, 2)


def print_receipt(items: List[Dict[str, Any]], customer_type: str, delivery: str) -> str:
    """Format and return a printable text receipt for the order."""
    amount = order_total(items, customer_type, delivery)
    lines = ['ORDER RECEIPT']
    
    for item in items:
        line_total = item['price'] * item['qty']
        lines.append(f"{item['qty']} x {item['name']} = {line_total}")
        
    lines.append(f"Customer: {customer_type}")
    lines.append(f"Delivery: {delivery}")
    lines.append(f"Total: {amount}")
    
    return '\n'.join(lines)
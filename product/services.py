# ORDER CREATION LOGIC

from django.core.exceptions import ValidationError
from .models import Order, Wallet

def create_order(user, product, quantity):
    # Quantity validation
    if quantity < 1:
        raise ValidationError("Quentity must be at least 1")
    
    # Product Active
    if not product.is_active:
        raise ValidationError("Product is not available")
    
    # Stock Check
    if product.quantity < quantity:
        raise ValidationError("Insufficient protuct Stock")
    
    # Wallet Mapped?
    if not product.wallet:
        raise ValidationError("Wallet is missing in the product")

    # User Wallet Exist?
    try:
        wallet = Wallet.objects.get(user=user)
    except Wallet.DoesNotExixt:
        raise ValidationError("User Wallet not Found")

    # Total Point calculate
    total_points = product.points * quantity

    # enough Points
    available_points = int(wallet.available_points)
    total_points = int(total_points)
    
    if available_points < total_points:
        raise ValidationError("Insufficient points in wallet")

    # All Good > Create Order

    order = Order.objects.create(
        user=user,
        product=product,
        quantity=quantity,
        total_points=total_points
    )

    # Update Wallet & Stock

    wallet.available_points -= total_points
    wallet.balance_points -= total_points
    wallet.save() 

    product.quantity -= quantity
    product.save()

    return order

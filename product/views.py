from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required

from .models import Product, Order
from .services import create_order


# Create your views here.

def product_list(request):
    products = Product.objects.filter(is_active=True)
    return render(request, "product/product_list.html", {"products":products})

    # context = {
    #     "products": products
    # }

    # return render(request, "product/product_list.html", context)

    
@login_required(login_url='login')
def product_detail(request, product_id):
    product = get_object_or_404(
        Product,
        id=product_id,
        is_active=True
    )

    if request.method =="POST":
        quantity = int(request.POST.get("quantity", 0))

        try:
            order = create_order(
                user=request.user,
                product=product,
                quantity=quantity
            )
            # messages.success(request, "Order Placed Seccussfully")
            return redirect("order_detail", order_id=order.id)
        
        except ValidationError as e:
            messages.error(request, e.message)
            

    # context= {
    #     "product": product
    # }

    return render(request, "product/product_detail.html", {"product": product})
    

def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    context = {
        "order": order
    }
    return render(request, "product/order_detail.html", context)

@login_required(login_url="login")
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "product/order_history.html", {"orders": orders})


from django.urls import path
from . import views
urlpatterns = [
    path('products/', views.product_list, name="product_list"),
    path('products/<int:product_id>/', views.product_detail, name="product_detail"),
    path('order/<int:order_id>/', views.order_detail, name="order_detail"),
    path('orders/', views.order_history, name="order_history")

]


from django.urls import path
from . import views

urlpatterns = [
    # Public pages
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    
    # Authentication
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    
    # Cart operations
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('update-cart/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('remove-cart/<int:item_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('clear-cart/', views.clear_cart, name='clear_cart'),
    
    # Checkout and orders
    path('checkout/', views.checkout, name='checkout'),
    path('buy-now/<int:product_id>/', views.buy_now, name='buy_now'),
    path('express-checkout/', views.express_checkout, name='express_checkout'),
    path('order-confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('orders/', views.order_history, name='order_history'),
    path('orders/cancel/<int:order_id>/', views.cancel_order, name='cancel_order'),
    
    # API Endpoints
    path('api/product/<int:product_id>/quick-view/', views.product_quick_view_api, name='product_quick_view_api'),
]

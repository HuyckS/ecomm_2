from django.urls import path
from . import views

urlpatterns = [
    # Customer routes
    path('', views.index),
    path('about', views.about),
    path('bulk', views.bulk),
    path('cart', views.cart),
    path('deals', views.deals),
    path('classes', views.classes),
    path('contact', views.contact),
    path('flowers', views.flowers),
    path('garden', views.garden),
    path('partner', views.partner),
    path('produce', views.produce),
    path('recipe', views.recipe),
    path('rotation', views.rotation),
    path('specialty', views.specialty),
    path('subscriptions', views.subscription),
    
    # Login/Register routes
    path('signIn', views.signIn),
    path('register', views.register),
    path('login', views.log_in),
    path('logout', views.log_out),
    path('success', views.success),

    # Product routes
    path('dashboard', views.dashboard),
    path('products/new', views.newProductForm),
    path('products/create', views.createProduct),
    path('products/<int:product_id>', views.showProduct),
    path('products/edit/<int:product_id>', views.editProduct),
    path('products/update/<int:product_id>', views.updateProduct),
    path('products/remove/<int:product_id>', views.removeProduct),

    # Payment routes
    path('add-to-cart', views.add_to_cart),
    path('remove/item/<int:item_id>', views.removeFromCart),
    path('checkout-session/create', views.create_checkout_session),
    path('payment/success', views.paymentSuccess),
    path('payment/failure', views.paymentFailure),
    path('history', views.orderHistory),
]

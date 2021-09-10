from django.urls import path
from . import views

urlpatterns = [
    # Customer routes
    path('', views.index),
    path('about', views.about),
    path('bulk', views.bulk),
    path('cart', views.cart),
    path('classes', views.classes),
    path('contact', views.contact),
    path('deals', views.deals),
    path('flowers', views.flowers),
    path('garden', views.garden),
    path('partner', views.partner),
    path('produce', views.produce),
    path('recipe', views.recipe),
    path('rotation', views.rotation),
    path('specialty', views.specialty),
    path('subscriptions', views.subscriptions),
    
    # Login/Register routes
    # path('register', views.register),
    # path('login', views.log_in),
    # path('logout', views.log_out),
    # path('success', views.success),

    # Product routes
    path('dashboard', views.dashboard),
    path('products/new', views.newProductForm),
    path('products/create', views.createProduct),
    path('products/<int:product_id>', views.showProduct),
    path('products/edit/<int:product_id>', views.editProduct),
    path('products/update/<int:product_id>', views.updateProduct),
    path('products/remove/<int:product_id>', views.removeProduct)
]

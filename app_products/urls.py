from django.urls import path
from . import views

urlpatterns = [
    # Customer routes
    path('about', views.index),
    path('bulk', views.index),
    path('cart', views.index),
    path('classes', views.index),
    path('contact', views.index),
    path('deals', views.index),
    path('flowers', views.index),
    path('garden', views.index),
    path('index', views.index),
    path('partner', views.index),
    path('produce', views.index),
    path('recipe', views.index),
    path('rotation', views.index),
    path('specialty', views.index),
    path('subscriptions', views.index),
    
    # Login/Register routes
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
    path('products/remove/<int:product_id>', views.removeProduct)
]

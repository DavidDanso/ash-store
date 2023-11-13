from django.urls import path
from . import views

urlpatterns = [
    path('', views.homePage, name='home'),
    path('products', views.productsPage, name='products'),
    path('cart', views.cartPage, name='cart'),
    path('checkout', views.checkoutPage, name='checkout'),

    path('update_item', views.updateItem, name='update_item'),
    path('process_order', views.processOrder, name='process_order'),
]
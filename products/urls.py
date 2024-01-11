from django.urls import path, re_path
from .views import (
    register_seller, 
    add_product, 
    list_products,
    login_user,
    logout_user,
    edit_product,
    view_cart,
    add_to_cart,
    login_as_guest,
    custom_404
)

urlpatterns = [
    path('', register_seller, name='register_seller'),
    path('add_product/', add_product, name='add_product'),
    path('list_products/', list_products, name='list_products'),
    path('login/', login_user, name='custom_login'),
    path('logout/', logout_user, name='custom_logout'),
    path('edit_product/<int:product_id>/', edit_product, name='edit_product'),
    
    path('login_as_guest/', login_as_guest, name='login_as_guest'),
    path('view_cart/', view_cart, name='view_cart'),
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    
    re_path(r'^.*/$', custom_404),
]
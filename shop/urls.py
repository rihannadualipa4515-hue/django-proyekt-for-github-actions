from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("catalog/", views.product_list, name="catalog"),
    path("catalog/<slug:slug>/", views.product_list, name="category"),
    path("product/<slug:slug>/", views.product_detail, name="product_detail"),
    path("cart/", views.cart_view, name="cart"),
    path("cart/add/<int:pk>/", views.cart_add, name="cart_add"),
    path("cart/remove/<str:key>/", views.cart_remove, name="cart_remove"),
    path("checkout/", views.checkout, name="checkout"),
    path("order/<int:pk>/", views.order_done, name="order_done"),
]

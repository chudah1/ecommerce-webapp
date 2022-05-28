from django.urls import path
from store import views

urlpatterns=[
    path("", views.home, name="home"),
    path("store/", views.store, name="store"),
    path("cart/", views.cart, name='cart'),
    path("checkout/", views.checkout, name="checkout"),
    path("login/", views.loginPage, name="login"),
    path("logout/", views.logoutPage, name="logout"),
    path("register/", views.register, name="register"),
    path("update_item/", views.updateItem, name="update_item"),
    path("process_order/", views.processOrder, name="process_order"),

]

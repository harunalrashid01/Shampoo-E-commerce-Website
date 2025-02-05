from django.urls import path
from .views import login_view, logout_view, home,signup_view, about,shop,contact_view,pp,terms
from . import views

urlpatterns = [
    path("signup/", signup_view, name="signup"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("home", home, name="home"),  # Protected home page
    path("about", about, name="about"),  # Protected home page
    path("shop", shop, name="shop"),  # Protected home page
    path("contact", contact_view, name="contact"),  # Protected home page
    path("privacypolicy", pp, name="pp"),  # Protected home page
    path("terms", terms, name="terms"),  # Protected home page
    path('subscribe/', views.subscribe_newsletter, name='subscribe_newsletter'),
    path('singleproduct/<int:product_id>/', views.singleproduct, name='sp'),
     path("shoppingcart/", views.shopping_cart, name="shoppingcart"),
     path("get-cart-products/", views.get_cart_products, name="get-cart-products"),
      path('api/cart/', views.cart_view, name='cart_view'),
      path('checkout/', views.checkout, name='checkout'),
        path('checkout/', views.checkout, name='checkout'),
    path('checkout/step-2/', views.checkout_step_2, name='checkout_step_2'),

]

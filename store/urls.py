from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),

    # Product Details
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),

    # Auth & Account
    path('login-signup/', views.login_signup_view, name='login_signup'),
    path('account/', views.account_view, name='account'),
    path('account/edit/', views.edit_account, name='edit_account'),
    path('logout/', views.logout_view, name='logout'),

    # Cart & Checkout
    path('cart/', views.cart_view, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('checkout/', views.checkout_view, name='checkout'),

    # Buy Now & Place Order
    path('buy-now/<slug:slug>/', views.buy_now, name='buy_now'),                     # Slug-based Buy Now
    path('place-order/<slug:slug>/', views.place_order_page, name='place_order_page'),  # Slug-based single order
    path('place-order/', views.place_order_page, name='place_order_from_cart'),         # Cart order
    path('order-success/', views.order_success, name='order_success'),
    path('reset-animation/', views.reset_animation, name='reset_animation'),
]
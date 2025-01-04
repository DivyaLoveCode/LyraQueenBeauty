from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('index/', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('search/', views.search, name='search'),  # Search route

    path('lipstick/', views.lipstick, name='lipstick'),
    path('nailpolish/', views.nailpolish, name='nailpolish'),
    path('kajol/', views.kajol, name='kajol'),
    path('eyeshadow/', views.eyeshadow, name='eyeshadow'),
    path('foundation/', views.foundation, name='foundation'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('enquiry/', views.enquiry, name='enquiry'),
    path('get-cart/', views.get_cart, name='get_cart'),
    path('save-cart/', views.save_cart, name='save_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('payment-gateway/<int:order_id>/', views.payment_gateway, name='payment-gateway'),
    path('payment-success/<int:order_id>/', views.payment_success, name='payment-success'),
    path('order-success/<int:order_id>/', views.order_success, name='order-success'),
]
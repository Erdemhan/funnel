from django.urls import path
from . import views

urlpatterns = [
    # Daha önce eklediğimiz URL'ler
    path('', views.home, name='home'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart_view, name='cart_view'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('purchase/', views.purchase, name='purchase'),
    path('lead_capture/', views.lead_capture, name='lead_capture'),
    # Yeni eklediğimiz URL
    path('stats/', views.stats_view, name='stats_view'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('', views.product_list, name='product_list'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('order/<int:pk>/', views.place_order, name='place_order'),
]

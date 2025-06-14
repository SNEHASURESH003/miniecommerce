from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    # path('logout/', views.user_logout, name='logout'),
    path('user-dashboard', views.dashboard, name='dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('add-product/', views.add_product, name='add_product'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('order/<int:pk>/', views.place_order, name='place_order'),
]

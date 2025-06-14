from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/user/', views.user_register, name='user_register'),
    path('register/admin/', views.admin_register, name='admin_register'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('add-product/', views.add_product, name='add_product'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('order/<int:pk>/', views.place_order, name='place_order'),
]

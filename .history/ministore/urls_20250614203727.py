from django.urls import path
from . import views

urlpatterns = [
    # Home / Dashboard
    path('', views.dashboard, name='dashboard'),

    # User Authentication
    path('register/user/', views.user_register, name='user_register'),
    path('login/user/', views.user_login, name='login'),
    
    # Admin Authentication (superuser only can register admins)
    path('register/admin/', views.admin_register, name='admin_register'),
    
   

    # Logout
    path('logout/', views.user_logout, name='logout'),

    # Admin Product Management
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('add-product/', views.add_product, name='add_product'),

    # Product Viewing & Ordering
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('order/<int:pk>/', views.place_order, name='place_order'),
]

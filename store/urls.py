from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('categories/', views.category_list, name='category_list'),
    path('category/<int:category_id>/', views.category_products, name='category_products'),
    path('all/', views.product_list, name='product_list'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
]

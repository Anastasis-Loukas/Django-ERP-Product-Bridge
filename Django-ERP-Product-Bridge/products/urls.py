from django.urls import path
from . import views

app_name = "products"

urlpatterns = [
    path('',views.products_home,name='home'),
    path('list/', views.products_list, name='list'),
    path('create/', views.create_product, name='create'),
    path('edit/<int:pk>/', views.edit_product, name='edit'),
    path('delete/<int:pk>/', views.delete_product, name='delete'),
]
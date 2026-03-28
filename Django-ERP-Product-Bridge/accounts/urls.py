from django.urls import path
from . import views


# URL patterns for authentication and main application views
urlpatterns = [
    path('', views.home_view),  # Root URL
    path('login/', views.login_view, name='login'),
    path('home/', views.home_view, name='home'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
]
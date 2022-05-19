from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='main'),
    path('login', views.registration, name='login'),
    path('logout', views.user_logout, name='logout'),
    path('guide', views.guide, name='guide'),
    path('soon', views.soon, name='soon'),
    path('test_login_register', views.test_login_register, name='test_login_register'),
    path('test_index', views.test_index, name='test_index'),
]
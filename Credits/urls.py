from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='main'),
    path('login', views.login, name='login'),
    path('guide', views.guide, name='guide'),
    path('soon', views.soon, name='soon'),
    path('test', views.test)
]
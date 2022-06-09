from django.urls import path
from . import views


boosts_list = views.BoostViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

boost_details = views.BoostViewSet.as_view({
    'get': 'retrieve',
    'put': 'partial_update',
    'delete': 'destroy',
})

urlpatterns = [
    path('', views.index, name='main'),
    path('login', views.registration, name='login'),
    path('logout', views.user_logout, name='logout'),
    path('guide', views.guide, name='guide'),
    path('soon', views.soon, name='soon'),
    path('core', views.get_core, name="core"),
    path('update_coins', views.update_coins, name="update_coins"),
    path('boosts', boosts_list, name='boosts'),
    path('boosts/<int:pk>', boost_details, name='boosts'),
]
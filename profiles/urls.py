from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile, name='profile'),
    path('add_friend/', views.add_friend, name='add_friend'),
    path('accept_friend/', views.accept_friend, name='accept_friend'),
    path('delete_friend/', views.delete_friend, name='delete_friend'),
]

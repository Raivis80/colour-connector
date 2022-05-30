from django.urls import path
from .import views

urlpatterns = [
    path('', views.profile, name='profile'),
    path('search_user/', views.search_user, name='search_user'),
    path('change_mood/', views.change_mood, name='change_mood'),
    path('change_color/', views.change_color, name='change_color'),
    path('add_friend/', views.add_friend, name='add_friend'),
    path('send_message/', views.send_message, name='send_message'),
    path('accept_friend/', views.accept_friend, name='accept_friend'),
    path('delete_friend/', views.delete_friend, name='delete_friend'),
    path("<slug:slug>", views.user_profile, name="user_profile"),
    path('<slug:slug>/', views.post_detail, name='post_detail')
]
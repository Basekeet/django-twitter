from django.contrib import admin
from django.urls import path

from .views  import remove_friend, profile_subs, profile_friends, get_profile, add_friend, create_post, register, user_login, profile, index, change_data, change_bio, change_username, user_logout

urlpatterns = [
    path('', index, name='index'),
    path('register/', register, name='user_register'),
    path('login/', user_login, name='user_login'),
    path('<str:username>/', profile, name='profile'),
    path('change_data/<str:username>/', change_data, name='change_data'),
    path('create_post/<str:username>/', create_post, name="create_post"),
    path('change_username', change_username, name='change_username'),
    path('change_bio', change_bio, name='change_bio'),
    path('add_friend/<str:username>/', add_friend, name='add_friend'),
    path('remvoe_friend/<str:username>/', remove_friend, name='remove_friend'),
    path('get_profile', get_profile, name='get_profile'),
    path('user_logout', user_logout, name='user_logout'),
    path("profile/<str:username>/subs", profile_subs, name='profile_subs'),
    path("profile/<str:username>/friends", profile_friends, name='profile_friends')
]
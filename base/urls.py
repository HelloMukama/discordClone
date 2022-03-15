from django.urls import path

from base.views import *

urlpatterns = [
    # Authentication of the Hosts of the specific rooms
    path('login/', login_page, name="login"),
    path('logout/', logout_user, name="logout"),
    path('register/', register_user, name="register"),

    path('', home, name="home"),
    path('room/<str:pk>/', room, name="room"),

    # user profile
    path('profile/<str:pk>', user_profile, name='user_profile'),

    # start CRUD  --- rooms
    path('create-room/', create_room, name="create_room"),
    path('update-room/<str:pk>/', update_room, name="update_room"),
    path('delete-room/<str:pk>/', delete_room, name="delete_room"),
    # end CRUD

    # start CRUD  --- mesages
    # path('update-room/<str:pk>/', update_room, name="update_room"),
    path('delete-message/<str:pk>/', delete_message, name="delete_message"),
    # end CRUD

    # update user profile
    path('update-user/<str:pk>/', update_user, name="update_user"),

    # mobile view- topics page
    path('topics/', topics_page, name="topics_page"),

    # mobile view- activities page
    path('activities/', activities_page, name="activities_page"),
]


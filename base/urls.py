from django.urls import path

from base.views import *

urlpatterns = [
    path('', home, name="home"),
    path('room/<str:pk>/', room, name="room"),
    path('create-room/', create_room, name="create_room"),
    path('update-room/<str:pk>/', update_room, name="update_room"),
    path('delete-room/<str:pk>/', delete_room, name="delete_room"),
]

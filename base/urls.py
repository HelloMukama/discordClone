from django.urls import path

import views

urlpatterns = [
    path('', views.home, name="home"),
    path('room /', views.room, name="room"),
]

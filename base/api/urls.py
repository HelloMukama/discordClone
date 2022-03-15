from django.urls import path

# from . import views
from base.api.views import *

urlpatterns = [
    path('', get_routes),  # loads at 'api/'
    path('rooms/', get_rooms),
    path('rooms/<str:pk>/', get_room),
]

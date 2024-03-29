from django.forms import ModelForm
from django.contrib.auth.models import User

from .models import Room


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']


class UserUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

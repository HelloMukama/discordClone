from django.shortcuts import render, redirect
from django.http import HttpResponse

from.forms import RoomForm
from .models import Room, Topic

rooms = [
    {'id': 1, 'name': 'Lets Learn Python'},
    {'id': 2, 'name': 'Design with Me'},
    {'id': 3, 'name': 'Front-End Developers'}
]


def home(request):
    rooms = Room.objects.all()
    topics = Topic.objects.all()
    context = {'rooms': rooms, 'topics': topics}
    return render(request, 'base/home.html', context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    context = {'room': room}
    return render(request, "base/room.html", context)


def create_room(request):
    form = RoomForm
    if request.method == 'POST':
        # print(request.POST)  # this is going to get printed to the terminal
        form = RoomForm(request.POST)   # adding the data to the form
        if form.is_valid():
            form.save()
            return redirect('home')  # redirect user to the homepage after room delete

    context = {'form': form}
    return render(request, "base/room_form.html", context)


def update_room(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)  # this here means that this form shall be prefilled with the room value

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)

        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)


def delete_room(request, pk):
    room = Room.objects.get(id=pk)

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/room_delete.html', {'obj': room})

from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm

from .forms import RoomForm, UserUpdateForm
from .models import Room, Topic, Message


def login_page(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')  # if user is logged in, take them to home page.

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User Does not exist!")  # flash msg

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)  # creates a session in the db and in the browser
            return redirect('home')
        else:
            messages.error(request, "Username or Password is Incorrect!")  # flash msg

    context = {'page': page}
    return render(request, 'base/login.html', context)


def logout_user(request):
    logout(request)
    return redirect('login')


def register_user(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Error occurred during registration')
    return render(request, 'base/register.html', {'form': form})


def home(request):
    q = request.GET.get('q') if request.GET.get('q') is not None else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    room_count = rooms.count()
    topics = Topic.objects.all()[0:5]
    # room_messages = Message.objects.all()   # display all messages
    # line below displays an activity as per the chosen room in the search bar
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    context = {'rooms': rooms,
               'topics': topics,
               'room_count': room_count,
               'room_messages': room_messages
               }
    return render(request, 'base/home.html', context)


@login_required(login_url='/login')
def room(request, pk):
    room = Room.objects.get(id=pk)
    # line below returns all the set of messages related to a particular room
    room_messages = room.message_set.all().order_by('-created')  # 12m r/ship
    participants = room.participants.all()   # m2m r/ship

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        """At this point, recall that someone is not a participant in a room by default
        So what happens is that after you comment, you're supposed to automatically be
        added to the room's participants and its what we are going to do on next line"""
        room.participants.add(request.user)  # adds this user to participants list
        return redirect('room', pk=room.id)

    context = {'room': room, 'room_messages': room_messages, 'participants': participants}
    return render(request, "base/room.html", context)


def user_profile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()  # this will return a set of all rooms 12m r/ship
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user,
               'rooms': rooms,
               'room_messages': room_messages,
               'topics': topics
               }
    return render(request, 'base/profile.html', context)


@login_required(login_url='/login')
def create_room(request):
    form = RoomForm
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        description = request.POST.get('description')
        name = request.POST.get('name')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=name,
            description=description
        )
        # # print(request.POST)  # this is going to get printed to the terminal
        # form = RoomForm(request.POST)  # adding the data to the form
        # if form.is_valid():
        #     # below we create an instance of the room
        #     room = form.save(commit=False)   # wait to log into db
        #     room.host = request.user  # logged in user only can create a room
        #     form.save()  # now save the room
        # return redirect('home')

        return redirect('home')  # redirect user to the homepage after room delete

    topics = Topic.objects.all()
    context = {'form': form, 'topics': topics}
    return render(request, "base/room_form.html", context)


@login_required(login_url='/login')
def update_room(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)  # this here means that this form shall be prefilled with the room value

    if request.user != room.host:
        return HttpResponse('You cant edit this')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')

        room.save()

        # form = RoomForm(request.POST, instance=room)
        # if form.is_valid():
        #     form.save()
        # return redirect('home')

        return redirect('home')

    topics = Topic.objects.all()
    context = {'form': form, 'topics': topics, 'room': room}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='/login')
def delete_room(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('You cant delete this')

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': room})


@login_required(login_url='/login')
def delete_message(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('You cant delete this')

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    # recall delete.html here is meant to be flexible
    return render(request, 'base/delete.html', {'obj': message})


@login_required(login_url='/login')
def update_user(request, pk):
    user = request.user
    form = UserUpdateForm(instance=user)

    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)

        if form.is_valid():
            form.save()
            return redirect('user_profile', pk=user.id)
    return render(request, 'base/edit_user.html', {'form': form})


def topics_page(request):
    q = request.GET.get('q') if request.GET.get('q') is not None else ''

    topics = Topic.objects.filter(Q(name__icontains=q))
    context = {'topics': topics}
    return render(request, 'base/topics.html', context)


def activities_page(request):
    room_messages = Message.objects.all()
    context = {'room_messages': room_messages}
    return render(request, 'base/activity.html', context)

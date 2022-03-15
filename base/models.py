from django.db import models

from django.contrib.auth.models import User


class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)  # someone who will host the room
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)  # the topic under which a room shall be
    name = models.CharField(max_length=200)  # name of a room
    # Recall below, null is for the db while blank is for the save method...
    description = models.TextField(null=True, blank=True)  # description of a room
    """ below, related_name means that we will not be using 'user' 
    e,g room.user when referencing the participants 
    since both are pointing to the same User model. 
    We have to choose another one to use i,e we've decided to use 'participants' """
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    created = models.DateTimeField(auto_now_add=True)  # recorded once
    updated = models.DateTimeField(auto_now=True)  # recorded each time an instance is saved

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return str(self.name)


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)  # recorded once
    updated = models.DateTimeField(auto_now=True)  # recorded each time an instance is saved

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.body[0:50]   # here the preview will return the first 50 characters

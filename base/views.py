from django.http import HttpResponse


def home(request):
    return HttpResponse('base page')


def room(request):
    return HttpResponse('Room page')
from rest_framework.decorators import api_view
from rest_framework.response import Response

from base.models import Room

from .serializers import RoomSerializer


@api_view(['GET'])   # only allowing a GET request
def get_routes(request):
    routes = [
        "GET /api",     # endpoint 1
        "GET /api/rooms",     # endpoint 2
        "GET /api/rooms/:id"  # endpoint 3
    ]
    return Response(routes)


@api_view(["GET"])   # only allowing a GET request
def get_rooms(request):
    rooms = Room.objects.all()  # from here, these will now be accessible via an api
    ''' Many below asks if there are going to be many objects that will be serialized
     And 'True' in this case means we are serializing more than one object'''
    serializer = RoomSerializer(rooms, many=True)
    return Response(serializer.data)  # here this means that you want to view the data in a serialized format


@api_view(["GET"])
def get_room(request, pk):   # here, we'll be getting serialised data of 1 object
    rooms = Room.objects.get(id=pk)
    serializer = RoomSerializer(rooms, many=False)
    return Response(serializer.data)

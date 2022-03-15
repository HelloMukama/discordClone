from rest_framework.serializers import ModelSerializer
from base.models import Room


class RoomSerializer(ModelSerializer):
    """ At this point, the model is going to be serialized so that its
    object data can be turned into json data that can be accessed via an api """
    class Meta:
        model = Room
        fields = '__all__'  # turn all fields into json objects. i.e Serialize the model



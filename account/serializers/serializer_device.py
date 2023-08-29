from rest_framework import serializers
from ..models import DeviceModel
from .serializer_user import UserSerializer


class DeviceSerializer(serializers.ModelSerializer):

    class Meta:
        model = DeviceModel
        fields = '__all__'

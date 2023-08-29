from rest_framework import serializers
from ..models import UserModel as User
from ..mixins.update import UpdateMixin


class UserSerializer(UpdateMixin,serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password', 'two_fa_secret')
        allow_update_fields = ['first_name', 'last_name', 'phone']

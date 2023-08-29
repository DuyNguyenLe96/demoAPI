from rest_framework import serializers
from django.contrib.auth import authenticate
from ..models import UserModel
import re


class LoginSerializer(serializers.Serializer):
    def validate_email(self, value):
        pat = re.compile(r"^\S+@\S+$")
        if not re.fullmatch(pat, value):
            raise serializers.ValidationError("Email is not valid")
        return value

    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)

    # def validate(self, attrs):
    #     email = attrs.get('email')
    #     password = attrs.get('password')
    #     if email and password:
    #         user = authenticate(email=email, password=password)
    #         if not user:
    #             raise serializers.ValidationError("username or password wrong", code='authorization')
    #     else:
    #         raise serializers.ValidationError("email or password is blank", code='authorization')
    #     attrs['user'] = user
    #     return attrs

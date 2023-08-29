from rest_framework import serializers
import re
from rest_framework.response import Response
from rest_framework import status
from ..models import UserModel as User


class SendMailToResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ResetPasswordSerializer(serializers.Serializer):
    def validate_password(self, value):
        pat = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$%&*?!])[A-Za-z\d!@$%&*?]{12,25}$")
        if not re.fullmatch(pat, value):
            raise serializers.ValidationError('Password must have atleast one special character,'
                                              ' one number, one uppercase,'
                                              'one lowercase and length beetween 12 and 25')
        return value

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("email and password shoudn't be same")
        return data

    password = serializers.CharField()
    confirm_password = serializers.CharField()


class ResetPasswordV2Serializer(serializers.Serializer):
    def validate_password(self, value):
        pat = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@$%&*?])[a-zA-Z\d!@$%&?*]{12,25}$")
        if not re.fullmatch(pat, value):
            raise serializers.ValidationError('Password must have atleast one special character,'
                                              ' one number, one uppercase,'
                                              'one lowercase and length beetween 12 and 25')
        return value

    code = serializers.CharField()
    password = serializers.CharField()

# def create(self, validated_data):
#     user = User(**validated_data)
#     user.set_password(validated_data['password'])
#     user.save()
#     return user

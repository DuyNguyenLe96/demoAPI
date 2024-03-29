from rest_framework import serializers


class OTPVerifySerializer(serializers.Serializer):
    code = serializers.CharField(max_length=6)
    ticket = serializers.CharField(max_length=255)


class OTPRefreshSerializer(serializers.Serializer):
    ticket = serializers.CharField(max_length=255)

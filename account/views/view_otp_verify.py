from rest_framework.views import APIView
from rest_framework.response import Response
from ..serializers import OTPVerifySerializer
from rest_framework.permissions import AllowAny
from rest_framework import status
from ..libs.ticket import take_user_id_from_ticket
from rest_framework_simplejwt.tokens import RefreshToken
from ..models import UserModel
from django.core.cache import cache
from ..serializers import UserSerializer


class OTPVerifyView(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        serializer = OTPVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data

        code = cache.get(data['ticket'])

        if code is None:
            return Response({
                'error': 'Ticket is not valid or expired',
            }, status=status.HTTP_400_BAD_REQUEST)

        if code != data['code']:
            return Response({
                'error': 'Invalid OTP code'
            }, status=status.HTTP_400_BAD_REQUEST)

        userID = take_user_id_from_ticket(data['ticket'])
        user = UserModel.objects.get(pk=userID)

        cache.delete(data['ticket'])

        refresh = RefreshToken.for_user(user)
        user_serializer = UserSerializer(user)

        return Response({
            'status': 'verified',
            'user': user_serializer.data,
            'token': {
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }
        }, status=status.HTTP_200_OK)

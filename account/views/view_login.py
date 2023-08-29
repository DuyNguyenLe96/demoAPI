from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from ..serializers import LoginSerializer

from ..libs.device import store_device
from ..libs.ticket import generate_ticket
from ..libs.otp import generate_otp_code
from ..libs.mail import send_mail_with_otp

from django.core.cache import cache


class LoginView(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        # 1.validate data
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 2. Check user password is valid?
        credentials = serializer.validated_data
        print(21, credentials)
        user = authenticate(**credentials)
        if user is None:
            return Response({
                'message': 'The username or password is incorrect',
            }, status=status.HTTP_400_BAD_REQUEST)

        # gen ra ticket va otp de gui mail(OTP) cho nguoi dung va return response
        # save device with user id
        device = store_device(request, user)
        print('device', device)
        ticket = generate_ticket(user, device)
        code = generate_otp_code()
        print("code--------------")
        print(code)

        if send_mail_with_otp(code, user.email):
            # save ticket in cache
            cache.set(ticket, code, timeout=60)
            return Response({
                'message': 'Email verify required',
                'ticket': ticket
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': True,
                'error_message': 'Error sending OTP',
            }, status=status.HTTP_400_BAD_REQUEST)

    """
    def post(self, request):
       serializer = LoginSerializer(data=request.data)
       serializer.is_valid(raise_exception=True)
       user = serializer.validated_data['user']
       print(serializer.validated_data['email'])
       print(user)
       refresh = RefreshToken.for_user(user)
       response_data = {
           "notification": "Login sucess",
       }
       response = Response(response_data)
       response['Authorization'] = f'Bearer {refresh.access_token}'

       return response
   """

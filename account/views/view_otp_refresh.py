from django.core.cache import cache

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from ..serializers import OTPRefreshSerializer

from ..models import UserModel

from ..libs.device import store_device, get_device
from ..libs.otp import generate_otp_code
from ..libs.mail import send_mail_with_otp
from ..libs.ticket import generate_ticket, take_user_id_from_ticket


class OTPRefreshView(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        # check ticket is invalid
        serializer = OTPRefreshSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data

        timeout = cache.ttl(data['ticket'])
        user_id = take_user_id_from_ticket(data['ticket'])
        user = UserModel.objects.get(pk=user_id)
        print('time out', timeout)
        print('cache', cache.get(data['ticket']))
        if timeout != 0:
            return Response({
                'ticket': data['ticket'],
                'timeout': timeout
            }, status.HTTP_400_BAD_REQUEST)

        device = store_device(request, user)
        ticket = generate_ticket(user, device)
        code = generate_otp_code()
        print("________Refresh OTP:", code)

        if send_mail_with_otp(code, user.email):
            cache.set(ticket, code, timeout=60)
            print('ttl', cache.ttl(ticket))
            return Response({
                'has_otp': True,
                'ticket': ticket,

            })
        else:
            return Response({
                'message': 'Error sending OTP'
            }, status.HTTP_400_BAD_REQUEST)

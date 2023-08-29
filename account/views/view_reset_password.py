from rest_framework.views import Response
from ..libs.mail import send_mail_with_link_reset_password
from rest_framework.views import APIView
from ..serializers import SendMailToResetPasswordSerializer
from ..libs.ticket import generate_ticket, take_user_id_from_ticket
from ..models import UserModel, DeviceModel
from rest_framework import status
from ..serializers import DeviceSerializer, UserSerializer, ResetPasswordSerializer, ResetPasswordV2Serializer
from django.core.cache import cache
from ..libs.otp import generate_otp_code
from ..libs.mail import send_mail_with_otp


class SendMailToResetPasswordView(APIView):
    def post(self, request):
        serializer = SendMailToResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = UserModel.objects.get(email=serializer.data['email'])
        print(user, user.id)
        if user is None:
            return Response({
                'error': 'Email is invalid'
            }, status=status.HTTP_404_NOT_FOUND)
        device = DeviceModel.objects.filter(user__id=user.id)
        device_dict = dict(device.values()[device.count() - 1])
        print(20, device_dict)
        ticket = generate_ticket(user=user, device=device_dict)
        print('ticket', ticket)

        send_mail = send_mail_with_link_reset_password(user, device_dict['ip'], ticket)
        if not send_mail:
            return Response({
                'error': "Send mail had error,server email maybe has error"
            }, status=status.HTTP_500)
        return Response({
            'status': 'Success send mail to reset password, check your email',
            'ticket': ticket
        }, status=status.HTTP_200_OK)


class ResetPasswordView(APIView):
    def post(self, request, ticket):
        print('reset password ticket: ', ticket)
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(serializer.data['password'])
        try:
            user_id = take_user_id_from_ticket(ticket)
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        user = UserModel.objects.get(id=user_id)
        print('user', user.email)
        if user is None:
            return Response({
                'error': "User doesn't exist"
            })
        print('password', user.password)
        user.set_password(serializer.data['password'])
        user.save()
        return Response({
            'message': 'Password reset successfully',
        }, status=status.HTTP_200_OK)


class SendMailToResetPasswordV2View(APIView):
    def post(self, request):
        serializer = SendMailToResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = UserModel.objects.get(email=serializer.data['email'])
        print(user, user.id)
        if user is None:
            return Response({
                'error': 'Email is invalid'
            }, status=status.HTTP_404_NOT_FOUND)
        device = DeviceModel.objects.filter(user__id=user.id)
        device_dict = dict(device.values()[device.count() - 1])
        print(20, device_dict)
        ticket = generate_ticket(user=user, device=device_dict)
        print('ticket', ticket)

        send_mail = send_mail_with_link_reset_password(user, device_dict['ip'], ticket)
        if not send_mail:
            return Response({
                'error': "Send mail had error,server email maybe has error"
            }, status=status.HTTP_500)
        code = generate_otp_code()
        print('reset password code', code)
        if send_mail_with_otp(code, user.email):
            cache.set(ticket, code, timeout=60)
            return Response({
                'status': 'Success send mail to reset password, check your email',
                'ticket': ticket,
                'has_otp': True
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'message': 'Error sending'
            })


class ResetPasswordV2View(APIView):
    def post(self, request, ticket):
        serializer = ResetPasswordV2Serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = serializer.data['code']
        timeout = cache.ttl(ticket)
        otp = cache.get(ticket)
        if timeout == 0 or code != otp:
            return Response({
                'error': 'OTP is expire or not match'
            }, status=status.HTTP_400_BAD_REQUEST)
        user_id = take_user_id_from_ticket(ticket)
        user = UserModel.objects.get(id=user_id)
        user.set_password(serializer.data['password'])
        user.save()
        return Response({
            'message': 'Change password successfully'
        },
            status=status.HTTP_200_OK)

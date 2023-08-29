from django.urls import path, include
from .views import RegisterView, LoginView, OTPRefreshView, OTPVerifyView, SendMailToResetPasswordView, \
    ResetPasswordView

urlpatterns = [
    path('account/', include([
        path('register', RegisterView.as_view(), name='register'),
        path('login', LoginView.as_view(), name='Login'),
        path('otp/', include([
            path('refresh', OTPRefreshView.as_view(), name='otp_refresh'),
            path('verify', OTPVerifyView.as_view(), name='otp_verify'),
        ])),
        path('reset/', include([
            path('send-mail', SendMailToResetPasswordView.as_view(), name='send_mail_reset'),
            path('tk/<str:ticket>/', ResetPasswordView.as_view(), name='reset_password')
        ]))
    ]))
]

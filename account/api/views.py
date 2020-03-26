from rest_framework.views import APIView
from rest_framework.response import Response
from account.models import Authi, Account, Token
from django.contrib.auth import logout
from account.textlocal import sendSMS
import pyotp
import json
from account.api.serializers import AccountSerializer, AuthiSerializer
from rest_framework.permissions import IsAuthenticated
from django.utils.translation import ugettext_lazy as _
import logging

logger = logging.getLogger(__name__)

class OTPGenerator(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        data = {}
        num = json.loads(request.body)['number']

        if Authi.objects.filter(mobile_number=num).exists():
            Authi.objects.get(mobile_number=num).delete()
        secretKey = pyotp.random_base32()
        totp = pyotp.TOTP(secretKey, interval=1000000)
        otp = totp.now()
        message = otp + " is the OTP for brainonet account verification on your mobile number. W4Fc9njfi5C"
        resp = sendSMS('MYmp17Fn+I0-BmN5VgYIil5zKuGObFiBJC5bjnTLZC', num, 'BRONET', message)
        resp = json.loads(resp)
        print(resp)
        if resp['status'] == "success":
            data['response'] = resp['status']
            data['message'] = resp['message']
            temporary_auth = Authi()
            temporary_auth.mobile_number = num
            temporary_auth.otp = secretKey
            temporary_auth.save()
        else:
            data['response'] = _("response.error")
            data['error_message'] = _("msg.account.otp.not.send")

        return Response(data)


class OTPAuthenticate(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        data = {}
        info = AuthiSerializer(data=request.data)
        if info.is_valid(raise_exception=True):
            info = info.data
        otp = info.get('otp')
        mobile_no = info.get('mobile_number')
        try:

            user_otp = Authi.objects.get(mobile_number=mobile_no)
            if user_otp:
                secretKey = user_otp.otp
                totp = pyotp.TOTP(secretKey, interval=1000000)

                if totp.verify(otp):
                    user_otp.delete()
                    try:
                        user = Account.objects.get(mobile_number=mobile_no)
                        token = Token.objects.create(user=user)
                        data['response'] = _("response.success")
                        data['token'] = token.key
                        return Response(data)
                    except Account.DoesNotExist:
                        user = Account()
                        user.mobile_number = mobile_no
                        user.save()
                        token = Token.objects.create(user=user)
                        data['response'] = _("response.success")
                        data['token'] = token.key
                        return Response(data)
                    except Token.DoesNotExist:
                        data['response'] = _("response.error")
                        data['error_message'] = _("msg.account.token.expired")
                        return Response(data)
                else:
                    data['response'] = _("response.error")
                    data['error_message'] = _("msg.account.otp.invalid")
                    return Response(data)

        except Authi.DoesNotExist:
            data['response'] = _("response.error")
            data['error_message'] = _("msg.account.otp.expired")
            return Response(data)


class Login(APIView):

    # authentication_classes = []
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = {}
        info = AccountSerializer(data=request.data)

        if info.is_valid(raise_exception=True):
            info = info.data
        first_name = info.get('first_name')
        last_name = info.get('last_name')
        try:
            user = request.user
            user.first_name = first_name
            user.last_name = last_name
            token = request.auth
            user.save()
            data['response'] = _("msg.welcome")
            data['token'] = token.key
            return Response(data)
        except Account.DoesNotExist:
            data['response'] = _("response.error")
            data['error_message'] = _("msg.account.not.found")
            return Response(data)
        except Token.DoesNotExist:
            data['response'] = _("response.error")
            data['error_message'] = _("msg.account.token.expired")
            return Response(data)


class Logout(APIView):

    # authentication_classes = []
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = {}
        try:
            request.auth.delete()
            logout(request)
            data['response'] = _("response.success")
            data['message'] = _("msg.account.logout.success")
            return Response(data)
        except Token.DoesNotExist:
            data['response'] = _("response.error")
            data['error_message'] = _("msg.account.token.expired")
            return Response(data)


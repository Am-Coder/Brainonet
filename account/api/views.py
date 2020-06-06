from rest_framework.views import APIView
from rest_framework.response import Response
from account.models import Authi
import json
from account.api.serializers import AccountSerializer, AuthiSerializer
from account.permissions import IsUser, IsStaff, IsManager, IsAdministrator
from django.utils.translation import ugettext_lazy as _
import logging
from account.utils import otp_send, otp_authenticate, login_check, logout_check
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
logger = logging.getLogger(__name__)


class OTPGenerator(APIView):
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'number': openapi.Schema(type=openapi.TYPE_STRING, description='Mobile Number'),
        }
    ))
    def post(self, request):
        num = json.loads(request.body)['number']

        if Authi.objects.filter(mobile_number=num).exists():
            Authi.objects.get(mobile_number=num).delete()
        data = otp_send(num)
        return Response(data)


class OTPAuthenticate(APIView):
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(request_body=AuthiSerializer)
    def post(self, request):

        # IsCMS header to detect whether it is app login or CMS login
        is_cms = request.headers.get("IsCMS")
        info = AuthiSerializer(data=request.data)
        if info.is_valid(raise_exception=True):
            info = info.data
        otp = info.get('otp')
        mobile_no = info.get('mobile_number')
        data = otp_authenticate(otp, mobile_no, is_cms)
        return Response(data)


class Login(APIView):

    # authentication_classes = []
    permission_classes = [IsUser, IsStaff, IsManager, IsAdministrator]

    @swagger_auto_schema(request_body=AccountSerializer)
    def post(self, request):
        info = AccountSerializer(data=request.data)
        if info.is_valid(raise_exception=True):
            info = info.data
        first_name = info.get('first_name')
        last_name = info.get('last_name')
        data = login_check(request, first_name, last_name)
        return Response(data)


class Logout(APIView):

    # authentication_classes = []
    permission_classes = [IsUser, IsStaff, IsManager, IsAdministrator]

    def post(self, request):
        data = logout_check(request)
        return Response(data)


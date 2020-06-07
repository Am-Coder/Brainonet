import pytest
from account.utils import otp_authenticate
import pyotp
from django.utils.translation import ugettext_lazy as _
from account.models import Authi, Account, Group


@pytest.mark.django_db
def test_user_create():
    Account.objects.create(first_name='john', last_name='doe', mobile_number='+917988824457')
    assert Account.objects.count() == 1


# @pytest.mark.django_db
# def test_otp_send():
#     data = otp_send("+917988824457")
#     assert data['response'] == 'success'


@pytest.mark.django_db
def test_otp_authenticate_shouldAuthenticateUserCorrectly():
    secretKey = pyotp.random_base32()
    totp = pyotp.TOTP(secretKey, interval=1000000)
    otp = totp.now()
    num = "+917988824457"
    temporary_auth = Authi()
    temporary_auth.mobile_number = num
    temporary_auth.otp = secretKey
    temporary_auth.save()
    Group.objects.create(group_name="User")
    data = otp_authenticate(otp, num)
    print(data)
    assert data['response'] == _("response.success")
    assert not Authi.objects.filter(mobile_number=num)


@pytest.mark.django_db
def test_otp_authenticate_shouldReturnErrorWhenWrongUser():
    num = "+917988824457"
    otp = ""
    data = otp_authenticate(otp, num)
    assert data['response'] == _("response.error")

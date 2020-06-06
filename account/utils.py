import pyotp
from account.textlocal import sendSMS
import json
from django.utils.translation import ugettext_lazy as _
from account.models import Authi, Account, Token, MemeberShip, Group
from django.contrib.auth import logout

GROUP_USER = "User"
GROUP_STAFF = "Staff"
GROUP_MANAGER = "Manager"
GROUP_ADMINISTRATOR = "Administrator"


def otp_send(num):
    data = {}
    secretKey = pyotp.random_base32()
    totp = pyotp.TOTP(secretKey, interval=1000000)
    otp = totp.now()
    message = otp + " is the OTP for brainonet account verification on your mobile number. W4Fc9njfi5C"
    resp = sendSMS('MYmp17Fn+I0-BmN5VgYIil5zKuGObFiBJC5bjnTLZC', num, 'BRONET', message)
    resp = json.loads(resp)
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
    return data


def otp_authenticate(otp, mobile_no, is_cms=False):
    data = {}
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
                    data['first_name'] = user.first_name
                    data['last_name'] = user.last_name
                    if is_cms:
                        # If you are not a user then you can have atmost one role among organization job roles
                        member = MemeberShip.objects.exclude(group=Group.objects.get(group_name=GROUP_USER)).get(account=user)
                    else:
                        member = MemeberShip.objects.get(account=user, group=Group.objects.get(group_name=GROUP_USER))
                    data['role'] = member.group.group_name

                except Account.DoesNotExist:
                    user = Account()
                    user.mobile_number = mobile_no
                    user.save()
                    token = Token.objects.create(user=user)
                    MemeberShip.objects.create(account=user, group=Group.objects.get(group_name=GROUP_USER))
                    data['response'] = _("response.success")
                    data['token'] = token.key
                except Token.DoesNotExist:
                    data['response'] = _("response.error")
                    data['error_message'] = _("msg.account.token.expired")
                except MemeberShip.DoesNotExist:
                    data['response'] = _("response.error")
                    data['error_message'] = "Invalid Access"
                finally:
                    return data

            else:
                data['response'] = _("response.error")
                data['error_message'] = _("msg.account.otp.invalid")
                return data

    except Authi.DoesNotExist:
        data['response'] = _("response.error")
        data['error_message'] = _("msg.account.otp.expired")
        return data


def login_check(request, first_name, last_name):
    data = {}
    try:
        user = request.user
        user.first_name = first_name
        user.last_name = last_name
        token = request.auth
        user.save()
        data['response'] = _("msg.welcome")
        data['token'] = token.key
    except Account.DoesNotExist:
        data['response'] = _("response.error")
        data['error_message'] = _("msg.account.not.found")
    except Token.DoesNotExist:
        data['response'] = _("response.error")
        data['error_message'] = _("msg.account.token.expired")
    finally:
        return data


def logout_check(request):
    data = {}
    try:
        request.auth.delete()
        logout(request)
        data['response'] = _("response.success")
        data['message'] = _("msg.account.logout.success")
        return data
    except Token.DoesNotExist:
        data['response'] = _("response.error")
        data['error_message'] = _("msg.account.token.expired")
        return data

from django.urls import re_path
from .views import get_account_properties, OTPGenerator, OTPAuthenticate, Login, Logout, update_account_properties


app_name = 'account'

urlpatterns = [
    re_path(r'^getOTP/$', OTPGenerator.as_view(), name='get_otp'),
    re_path(r'^authOTP/$', OTPAuthenticate.as_view(), name='auth_otp'),
    re_path(r'^login/$', Login.as_view(), name='login'),
    re_path(r'^logout/$', Logout.as_view(), name='logout'),
    re_path(r'^accountProperties/$', get_account_properties, name='account_properties'),
    re_path(r'^updateAccountProperties/$', update_account_properties, name='update_account_properties'),
]

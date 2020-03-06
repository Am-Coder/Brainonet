from django.urls import re_path
from .views import *

from rest_framework.authtoken.views import obtain_auth_token

app_name = 'account'

urlpatterns = [
    re_path(r'^getOTP/$', OTPGenerator.as_view(), name='get_otp'),
    re_path(r'^authOTP/$', OTPAuthenticate.as_view(), name='auth_otp'),
    re_path(r'^login/$', Login.as_view(), name='login'),
    re_path(r'^logout/$', Logout.as_view(), name='logout'),

]









# urlpatterns = [
#   path('check_if_account_exists', does_account_exist_view, name="check_if_account_exists"),
#   path('properties', account_properties_view, name="properties"),
#   path('properties/update', update_account_view, name="update"),
#   path('login', ObtainAuthTokenView.as_view(), name='login'),
#   path('register', registration_view, name="register"),
# ]
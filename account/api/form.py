from django import forms


class MobileForm(forms.Form):
    number = forms.CharField(max_length="20", label="Give your Mobile Number")


class OtpForm(forms.Form):
    otp = forms.CharField(max_length=6, label="Give the OTP sent to your Mobile")



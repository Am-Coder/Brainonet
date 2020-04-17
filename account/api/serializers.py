from rest_framework import serializers

from account.models import Account, Authi


class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ['first_name', 'last_name']

    def validate_first_name(self, first_name):
        if len(first_name) > 20:
            raise serializers.ValidationError("Length Cannot be greater then 20")
        return first_name

    def validate_last_name(self, last_name):
        if len(last_name) > 20:
            raise serializers.ValidationError("Length Cannot be greater then 20")
        return last_name

    def save(self):
        account = Account(
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name']
        )

        account.save()
        return account


class AuthiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Authi
        fields = "__all__"
        # fields = ['mobile_number', 'otp']

    def validate_otp(self, otp):
        if len(otp) != 6:
            raise serializers.ValidationError("OTP length should be 6")
        return otp

    def validate_mobile_number(self, mobile_number):
        if len(mobile_number) >= 15:
            raise serializers.ValidationError("Mobile Number length incorrect")
        return mobile_number

    def save(self, **kwargs):
        otp = self.validated_data['otp']
        mobile = self.validated_data['mobile_number']

        temporary_auth = Authi(otp=otp, mobile_number=mobile)
        temporary_auth.save()


# class AccountPropertiesSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Account
#         fields = ['pk', 'email', 'username']

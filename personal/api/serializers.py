from rest_framework import serializers
from account.models import Account


class StaffDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['pk', 'first_name', 'last_name', 'mobile_number', 'date_joined']

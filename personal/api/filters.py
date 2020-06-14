from account.models import Account
from django_filters import rest_framework as filters


class StaffSearchFilter(filters.FilterSet):
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'mobile_number']

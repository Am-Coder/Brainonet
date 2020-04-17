from account.api.serializers import AccountSerializer, AuthiSerializer
import pytest
from account.models import Account, Authi


@pytest.fixture
def db_account_serializer():
    return [{'first_name': 'John', 'last_name': 'DoeDoeDoeDoeDoeDoeDoe'},
            {'first_name': 'JohnJohnJohnJohnJohnJ', 'last_name': 'Doe'},
            {'first_name': 'John', 'last_name': 'Doe'}]


@pytest.fixture
def db_authi_serializer():
    return [{'otp': '11111', 'mobile_number': '1111111111'},
            {'otp': '111111', 'mobile_number': '111111111111111111'},
            {'otp': '111111', 'mobile_number': '1111111111'}
            ]


@pytest.mark.django_db
def test_account_serializer_shouldValidateFirstName(db_account_serializer):
    serializer = AccountSerializer(data=db_account_serializer[1])

    assert not serializer.is_valid()
    assert serializer.validated_data == {}
    assert serializer.errors == {'first_name': ['Length Cannot be greater then 20']}


@pytest.mark.django_db
def test_account_serializer_shouldValidateLastName(db_account_serializer):
    serializer = AccountSerializer(data=db_account_serializer[0])

    assert not serializer.is_valid()
    assert serializer.validated_data == {}
    assert serializer.errors == {'last_name': ['Length Cannot be greater then 20']}


@pytest.mark.django_db
def test_account_serializer_shouldSaveValidatedAccount(db_account_serializer):
    serializer = AccountSerializer(data=db_account_serializer[2])
    assert serializer.is_valid()
    assert serializer.validated_data == db_account_serializer[2]
    serializer.save()
    assert Account.objects.count() == 1


@pytest.mark.django_db
def test_authi_serializer_shouldValidateOtp(db_authi_serializer):
    serializer = AuthiSerializer(data=db_authi_serializer[0])

    assert not serializer.is_valid()
    assert serializer.validated_data == {}
    assert serializer.errors == {'otp': ['OTP length should be 6']}


@pytest.mark.django_db
def test_authi_serializer_shouldValidateMobileNumber(db_authi_serializer):
    serializer = AuthiSerializer(data=db_authi_serializer[1])

    assert not serializer.is_valid()
    assert serializer.validated_data == {}
    assert serializer.errors == {'mobile_number': ['Mobile Number length incorrect']}


@pytest.mark.django_db
def test_authi_serializer_shouldSaveValidatedAuthi(db_authi_serializer):
    serializer = AuthiSerializer(data=db_authi_serializer[2])

    assert serializer.is_valid()
    assert serializer.validated_data == db_authi_serializer[2]
    serializer.save()
    assert Authi.objects.count() == 1

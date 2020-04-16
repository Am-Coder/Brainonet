import pytest
from account.models import Token, Account
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _


# Create your tests here.


@pytest.fixture
def test_mobile_num():
    return 'strong-test-pass'


@pytest.fixture
def create_user(db, test_mobile_num):
    def make_user(**kwargs):
        kwargs['mobile_number'] = test_mobile_num
        if 'first_name' not in kwargs:
            kwargs['first_name'] = 'John'
        if 'last_name' not in kwargs:
            kwargs['last_name'] = 'Doe'
        return Account.objects.create(**kwargs)

    return make_user


@pytest.fixture
def create_token(db, create_user):
    user = create_user()
    token, s = Token.objects.get_or_create(user=user)
    return token


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def auth_api_client(create_token):
    from rest_framework.test import APIClient
    api_client = APIClient()
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + create_token.key)
    return api_client


@pytest.mark.django_db
def test_login_view_shouldLogInAuthorizedUser(auth_api_client):
    url = reverse('account:login')
    response = auth_api_client.post(url, {'first_name': 'John', 'last_name': 'Doe'})
    data = response.data
    assert response.status_code == 200
    assert data['response'] == _("msg.welcome")


@pytest.mark.django_db
def test_unauthorized_request(api_client):
    url = reverse('account:login')
    response = api_client.get(url)
    assert response.status_code == 401


@pytest.mark.django_db
def test_logout_view_shouldLogOutAuthorizedUser(auth_api_client):
    url = reverse('account:logout')
    assert Token.objects.all().count() == 1
    response = auth_api_client.post(url)
    data = response.data
    assert response.status_code == 200
    assert data['response'] == _("response.success")
    assert Token.objects.all().count() == 0

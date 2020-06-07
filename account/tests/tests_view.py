import pytest
from account.models import Token, Group
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _


# Create your tests here.

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
    # Group.objects.create(group_name="User")
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

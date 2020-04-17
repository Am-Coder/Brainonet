import pytest
from account.models import Token, Account
from blog.models import Blog
from communities.models import Communities


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
def create_dataset(db):
    def make_dataset():
        community = Communities(name="Com")
        community.save()
        blog = Blog(title="Blog", community=community)
        blog.save()
        return blog, community

    return make_dataset

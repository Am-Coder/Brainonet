import pytest
from account.models import Token, Account
from blog.models import Blog
from communities.models import Communities
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from account.models import Group, MemberShip

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
        if 'mobile_number' not in kwargs:
            kwargs['mobile_number'] = test_mobile_num
        if 'first_name' not in kwargs:
            kwargs['first_name'] = 'John'
        if 'last_name' not in kwargs:
            kwargs['last_name'] = 'Doe'
        account, s = Account.objects.get_or_create(**kwargs)
        group, g = Group.objects.get_or_create(group_name="User")
        MemberShip.objects.create(account=account, group=group)
        return account

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


@pytest.fixture
def image_url():
    def img_url(url=None):
        if url:
            return url
        return "test.png"
    return img_url


@pytest.fixture
def in_memory_image(image_url):
    def make_image(url=None):
        url = image_url(url)
        img = Image.new('RGB', (512, 512))

        # create in memory image for testing
        new_image_io = BytesIO()
        img.save(new_image_io, format='PNG')
        img_file = ContentFile(new_image_io.getvalue(), url)
        return img_file

    return make_image


# So that images if not in-memory get removed
@pytest.fixture(autouse=True)
def clean_up(db):
    # Before Each Test - SetUp

    yield
    # After each test - TearDown
    Communities.objects.all().delete()
    Blog.objects.all().delete()


@pytest.fixture
def create_dataset_with_image(db, in_memory_image):
    def make_dataset():
        img = in_memory_image()
        community = Communities(name="Com")
        community.avatarimage = img
        community.backgroundimage = img
        community.save()
        blog = Blog(title="Blog", community=community)
        blog.image = img
        blog.save()
        return blog, community

    return make_dataset

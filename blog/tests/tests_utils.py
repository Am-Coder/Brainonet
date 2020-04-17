import pytest
from blog.models import Blog, Vote
from communities.models import Communities
from account.models import Account
from blog.utils import vote_handler, is_image_aspect_ratio_valid, is_image_size_valid


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


@pytest.mark.django_db
def test_vote_handler_shouldHandleVoteByUserOnBlog(create_user, create_dataset):
    user = create_user()
    blog, community = create_dataset()
    data, count = vote_handler(user, blog)
    assert Vote.objects.count() == 1
    assert data['status']
    assert count == 1

    data, count = vote_handler(user, blog)
    assert Vote.objects.count() == 0
    assert not data['status']
    # vote_handler() does not makes changes in blog object, it just tells whether to increase(+1) or
    # decrease(-1) the vote
    assert count == -1


def test_is_image_aspect_ratio_valid_shouldValidateImageAspectRaio():
    pass


def test_is_image_size_valid_shouldValidateImageSize():
    pass

import pytest
from blog.models import Vote
from blog.utils import vote_handler, is_image_aspect_ratio_valid, is_image_size_valid


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

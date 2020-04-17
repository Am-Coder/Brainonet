import pytest
from blog.models import Vote
from blog.utils import vote_handler, is_image_aspect_ratio_valid, is_image_size_valid
from PIL import Image
import os


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


def test_is_image_aspect_ratio_valid_shouldValidateImageAspectRaio(image_url):
    image_url = image_url()
    img = Image.new('RGB', (512, 512))
    img.save(image_url)
    right = is_image_aspect_ratio_valid(image_url)
    os.remove(image_url)

    img = img.resize((512, 1024))
    img.save(image_url)
    wrong = is_image_aspect_ratio_valid(image_url)
    os.remove(image_url)

    assert right
    assert not wrong


# Correct Test Format
def test_is_image_size_valid_shouldValidateImageSize(image_url):
    image_url = image_url()
    img = Image.new('RGB', (512, 512))
    img.save(image_url)
    image_size = os.path.getsize(image_url)
    max_size = image_size + 1
    rightsize = is_image_size_valid(image_url, max_size)
    max_size = image_size - 1
    wrongsize = is_image_size_valid(image_url, max_size)
    os.remove(image_url)
    assert rightsize
    assert not wrongsize

import cv2
import os
from blog.models import Blog, Vote
from django.utils.translation import ugettext_lazy as _


def is_image_aspect_ratio_valid(img_url):
    img = cv2.imread(img_url)
    dimensions = tuple(img.shape[1::-1])
    aspect_ratio = dimensions[0] / dimensions[1]
    print(dimensions)
    if aspect_ratio < 1:
        return False
    return True


def is_image_size_valid(img_url, mb_limit):
    image_size = os.path.getsize(img_url)

    if image_size > mb_limit:
        return False
    return True


def vote_handler(user, blog):
    data = {}
    count = blog.vote_count
    all_votes = Vote.objects.filter(blog=blog)
    data['response'] = _("response.success")
    if all_votes.filter(user=user).exists():
        all_votes.filter(user=user).delete()
        count -= 1
        data['status'] = False
    else:
        Vote.objects.create(user=user, blog=blog)
        count += 1
        data['status'] = True
    return data, count

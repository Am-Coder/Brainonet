import cv2
import numpy as np
from utilities.imsearch import colordescriptor, searcher, createdataset
from django.utils.translation import ugettext_lazy as _


def get_opencv_img_from_buffer(buffer, flags=-1):
    bytes_as_np_array = np.frombuffer(buffer.read(), dtype=np.uint8)
    return cv2.imdecode(bytes_as_np_array, flags)


def get_token_from_cookie(request):
    token = request.COOKIES.get("Authorization")
    if token:
        token = token.replace("Token%20", "")
    return token


def get_image_search_results(image):
    context = {}
    cd = colordescriptor.ColorDescriptor((8, 12, 3))
    features = cd.describe(image)
    results = searcher.Searcher().search(features, 3)
    if len(results) != 0:
        context['response'] = _("response.success")
        context['results'] = results
    else:
        context['response'] = _("response.error")
        context['error_message'] = _('msg.personal.fake.imagesearch.not.found')
    return context

import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.exceptions import ValidationError
from blog.utils import is_image_aspect_ratio_valid, is_image_size_valid


def image_validator(image, image_max_size=1024 * 1024 * 3):
    # In case the image already exists (Example :  /communitie/com-abc.png ) then we need image name only as
    # as we make use of temporary storage
    img = str(image).rsplit('/')[-1]
    url = os.path.join(settings.MEDIA_ROOT, img)
    storage = FileSystemStorage(location=url)
    with storage.open('', 'wb+') as destination:
        for chunk in image.chunks():
            destination.write(chunk)
        destination.close()
    if not is_image_size_valid(url, image_max_size):
        os.remove(url)
        raise ValidationError("That image is too large. Images must be less than 3 MB. Try a different image.")

    if not is_image_aspect_ratio_valid(url):
        os.remove(url)
        raise ValidationError("Image height must not exceed image width. Try a different image.")
    os.remove(url)

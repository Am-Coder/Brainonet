from rest_framework import serializers
from expose.models import Expose

import os
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.storage import FileSystemStorage
IMAGE_SIZE_MAX_BYTES = 1024*1024*3
MIN_TITLE_LENGTH = 5
MIN_BODY_LENGTH = 50

from blog.utils import is_image_aspect_ratio_valid, is_image_size_valid


class ExposeSerializer(serializers.ModelSerializer):

  exposeunit = serializers.SerializerMethodField('get_exposeunit_name')
  image = serializers.SerializerMethodField('validate_image_url')

  class Meta:
    model = Expose
    fields = ['pk', 'title', 'slug', 'body', 'image', 'date_updated', 'exposeunit']

  def get_exposeunit_name(self, expose):
    exposeunit = expose.exposeunit.name
    return exposeunit

  def validate_image_url(self, expose):
    image = expose.image
    new_url = image.url
    if "?" in new_url:
      new_url = image.url[:image.url.rfind("?")]
    return new_url


class ExposeUpdateSerializer(serializers.ModelSerializer):

  class Meta:
    model = Expose
    fields = ['title', 'body', 'image']

  def validate(slef, expose):
    try:
      title = expose['title']
      if len(title) < MIN_TITLE_LENGTH:
        raise serializers.ValidationError({"response": "Enter a title longer than " + str(MIN_TITLE_LENGTH) + " characters."})

      body = expose['body']
      if len(body) < MIN_BODY_LENGTH:
        raise serializers.ValidationError({"response": "Enter a body longer than " + str(MIN_BODY_LENGTH) + " characters."})

      image = expose['image']
      url = os.path.join(settings.TEMP, str(image))
      storage = FileSystemStorage(location=url)

      with storage.open('', "wb+") as destination:
        for chunk in image.chunks():
          destination.write(chunk)
        destination.close()

      if not is_image_size_valid(url, IMAGE_SIZE_MAX_BYTES):
        os.remove(url)
        raise serilizers.ValidationError({"response": "That image is too large. Images must be less than 3 MB. Try a different image."})

      
      if not is_image_aspect_ratio_valid(url):
        os.remove(url)
        raise serializers.ValidationError({"response": "Image height must not exceed image width. Try a different image."})

      os.remove(url)
    except KeyError:
      pass
    return expose


class ExposeCreateSerializer(serializers.ModelSerializer):

  class Meta:
    model = Expose
    fields = ['title', 'body', 'image', 'date_updated', 'exposeunit']

  def save(self):

    try:
      image = self.validated_data['image']
      title = self.validated_data['title']
      if len(title) < MIN_TITLE_LENGTH:
        raise serializers.ValidationError({"response": "Enter a title longer than " + str(MIN_TITLE_LENGTH) + " characters."})

      body = self.validated_data['body']
      if len(body) < MIN_BODY_LENGTH:
        raise serializers.ValidationError({"response": "Enter a body longer than " + str(MIN_BODY_LENGTH) + " characters."})

      expose = Expose(
              exposeunit = self.validated_data['exposeunit'],
              title = title,
              body = body,
              image = image,
      )

      url = os.path.join(settings.TEMP, str(image))
      storage = FileSystemStorage(location=url)

      with storage.open('', 'wb+') as destination:
        for chunk in image.chunks():
          destination.write(chunk)
        destination.close()

      if not is_image_size_valid(url, IMAGE_SIZE_MAX_BYTES):
        os.remove(url)
        raise serializers.ValidationError({"response": "That image is too large. Images must be less than 3 MB. Try a different image."})

      if not is_image_aspect_ratio_valid(url):
        os.remove(url)
        raise serializers.ValidationError({"response": "Image height must not exceed image width. Try a different image."})

      
      os.remove(url)
      expose.save()
      return expose
    except KeyError:
      raise serializers.ValidationError({"response": "You must have a title, some context, and an image."})
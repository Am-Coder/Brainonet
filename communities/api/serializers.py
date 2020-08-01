from rest_framework import serializers
from communities.models import Communities, CommunitySubscribers
from blog.models import Blog
from commons.api.serializers import DynamicFieldsModelSerializer
import os
from django.core.files.storage import default_storage, FileSystemStorage
from django.conf import settings

from blog.utils import is_image_aspect_ratio_valid, is_image_size_valid

IMAGE_SIZE_MAX_BYTES = 1024 * 1024 * 3
MIN_TITLE_LENGTH = 5
MIN_BODY_LENGTH = 50


class CommunitySerializer(DynamicFieldsModelSerializer):
    backgroundimage = serializers.SerializerMethodField('validate_backgroundimage_url')
    avatarimage = serializers.SerializerMethodField('validate_avatarimage_url')

    # Custom Serializer Field
    join = serializers.SerializerMethodField()
    posts = serializers.SerializerMethodField()

    class Meta:
        model = Communities
        fields = ['pk', 'name', 'slug', 'description', 'backgroundimage', 'subscriber_count',
                  'avatarimage', 'date_updated', 'join', 'posts']

    def validate_avatarimage_url(self, community):
        avatarimage = community.avatarimage
        new_url = avatarimage.url
        if "?" in new_url:
            new_url = avatarimage.url[:avatarimage.url.rfind("?")]
        return new_url

    def validate_backgroundimage_url(self, community):
        backgroundimage = community.backgroundimage
        new_url = backgroundimage.url
        if "?" in new_url:
            new_url = backgroundimage.url[:backgroundimage.url.rfind("?")]
        return new_url

    def get_join(self, obj):
        request = self.context['request']
        if request:
            return CommunitySubscribers.objects.filter(community=obj, user=request.user).exists()
        return False

    def get_posts(self, obj):
        if Blog.objects.filter(community=obj):
            return Blog.objects.filter(community=obj).count()
        return 0


class CommunityUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Communities
        fields = ['description', 'backgroundimage', 'avatarimage']

    def validate(self, community):
        try:
            image = community['backgroundimage']
            url = os.path.join(settings.TEMP, str(image))
            storage = FileSystemStorage(location=url)

            with storage.open('', "wb+") as destination:
                for chunk in image.chunks():
                    destination.write(chunk)
                destination.close()

            if not is_image_size_valid(url, IMAGE_SIZE_MAX_BYTES):
                os.remove(url)
                raise serializers.ValidationError(
                    {"response": "That image is too large. Images must be less than 3 MB. Try a different image."})

            if not is_image_aspect_ratio_valid(url):
                os.remove(url)
                raise serializers.ValidationError(
                    {"response": "Image height must not exceed image width. Try a different image."})

            os.remove(url)

            image = community['avatarimage']
            url = os.path.join(settings.TEMP, str(image))
            storage = FileSystemStorage(location=url)

            with storage.open('', "wb+") as destination:
                for chunk in image.chunks():
                    destination.write(chunk)
                destination.close()

            if not is_image_size_valid(url, IMAGE_SIZE_MAX_BYTES):
                os.remove(url)
                raise serializers.ValidationError(
                    {"response": "That image is too large. Images must be less than 3 MB. Try a different image."})

            if not is_image_aspect_ratio_valid(url):
                os.remove(url)
                raise serializers.ValidationError(
                    {"response": "Image height must not exceed image width. Try a different image."})

            os.remove(url)
        except KeyError:
            pass
        return community


class CommunityCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Communities
        fields = ['name', 'description', 'backgroundimage', 'avatarimage', 'date_updated']

    def save(self):

        try:
            backgroundimage = self.validated_data['backgroundimage']
            avatarimage = self.validated_data['avatarimage']
            name = self.validated_data['name']
            description = self.validated_data['description']
            community = Communities(
                name=name,
                backgroundimage=backgroundimage,
                avatarimage=avatarimage,
                description=description,
            )

            url = os.path.join(settings.TEMP, str(backgroundimage))
            storage = FileSystemStorage(location=url)

            with storage.open('', 'wb+') as destination:
                for chunk in backgroundimage.chunks():
                    destination.write(chunk)
                destination.close()

            if not is_image_size_valid(url, IMAGE_SIZE_MAX_BYTES):
                os.remove(url)
                raise serializers.ValidationError(
                    {"response": "That image is too large. Images must be less than 3 MB. Try a different image."})

            if not is_image_aspect_ratio_valid(url):
                os.remove(url)
                raise serializers.ValidationError(
                    {"response": "Image height must not exceed image width. Try a different image."})

            os.remove(url)
            community.save()
            return community
        except KeyError:
            raise serializers.ValidationError(
                {"response": "You must have name, backgroundimage, avatarimage and description for community."})

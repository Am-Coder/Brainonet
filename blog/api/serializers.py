from rest_framework import serializers
from blog.models import Blog, Comment

import os
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.storage import FileSystemStorage

IMAGE_SIZE_MAX_BYTES = 1024 * 1024 * 3
MIN_TITLE_LENGTH = 5
MIN_BODY_LENGTH = 50

from blog.utils import is_image_aspect_ratio_valid, is_image_size_valid


class BlogSerializer(serializers.ModelSerializer):
    community = serializers.SerializerMethodField('get_communtiy_name')
    image = serializers.SerializerMethodField('validate_image_url')

    class Meta:
        model = Blog
        fields = ['pk', 'title', 'slug', 'body', 'image', 'date_updated', 'community']

    def get_communtiy_name(self, blog):
        community = blog.community.name
        return community

    def validate_image_url(self, blog):
        image = blog.image
        new_url = image.url
        if "?" in new_url:
            new_url = image.url[:image.url.rfind("?")]
        return new_url


class BlogUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['title', 'body', 'image']

    def validate(self, blog):
        try:
            title = blog['title']
            if len(title) < MIN_TITLE_LENGTH:
                raise serializers.ValidationError(
                    {"response": "Enter a title longer than " + str(MIN_TITLE_LENGTH) + " characters."})

            body = blog['body']
            if len(body) < MIN_BODY_LENGTH:
                raise serializers.ValidationError(
                    {"response": "Enter a body longer than " + str(MIN_BODY_LENGTH) + " characters."})

            image = blog['image']
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
        return blog


class BlogCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['title', 'body', 'image', 'date_updated', 'community']

    def save(self):

        try:
            image = self.validated_data['image']
            title = self.validated_data['title']
            if len(title) < MIN_TITLE_LENGTH:
                raise serializers.ValidationError(
                    {"response": "Enter a title longer than " + str(MIN_TITLE_LENGTH) + " characters."})

            body = self.validated_data['body']
            if len(body) < MIN_BODY_LENGTH:
                raise serializers.ValidationError(
                    {"response": "Enter a body longer than " + str(MIN_BODY_LENGTH) + " characters."})

            blog = Blog(
                community=self.validated_data['community'],
                title=title,
                body=body,
                image=image,
            )

            url = os.path.join(settings.TEMP, str(image))
            storage = FileSystemStorage(location=url)

            with storage.open('', 'wb+') as destination:
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
            blog.save()
            return blog
        except KeyError:
            raise serializers.ValidationError({"response": "You must have a title, some content, and an image."})


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['comment']

    def validate_comment(self, comment):
        if len(comment) > 300:
            raise serializers.ValidationError("Comment length exceeded")
        return comment

    def save(self, **kwargs):
        print(kwargs)
        comment_text = self.validated_data['comment']
        print(comment_text)
        comment = Comment(comment=comment_text, user=kwargs['user'], blog=kwargs['blog'])
        comment.save()
        return comment

from rest_framework import serializers
from blog.models import Blog, Comment, References, TaggedBlogs, Vote

import os
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.storage import FileSystemStorage
from blog.utils import is_image_aspect_ratio_valid, is_image_size_valid
from account.api.serializers import AccountSerializer

IMAGE_SIZE_MAX_BYTES = 1024 * 1024 * 3
MIN_TITLE_LENGTH = 5
MIN_BODY_LENGTH = 50


class BlogSerializer(serializers.ModelSerializer):
    community = serializers.SerializerMethodField('get_communtiy_name')
    image = serializers.SerializerMethodField('validate_image_url')

    # Custom Fields
    vote = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()

    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(BlogSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    class Meta:
        model = Blog
        fields = ['pk', 'title', 'description', 'slug', 'body', 'image', 'date_updated',
                  'vote_count', 'view_count', 'community', 'vote', 'comment_count']

    def get_communtiy_name(self, blog):
        community = blog.community.name
        return community

    def validate_image_url(self, blog):
        image = blog.image
        new_url = image.url
        if "?" in new_url:
            new_url = image.url[:image.url.rfind("?")]
        return new_url

    def get_vote(self, obj):
        request = self.context['request']
        if request:
            return Vote.objects.filter(user=request.user).exists()
        return False

    def get_comment_count(self, obj):
        if Comment.objects.filter(blog=obj):
            return Comment.objects.filter(blog=obj).count()
        return 0


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
        if comment is None:
            raise serializers.ValidationError("Empty Comments not allowed")
        if len(comment) > 250:
            raise serializers.ValidationError("Maximum Comment length exceeded")
        return comment

    def save(self, **kwargs):
        print(kwargs)
        comment_text = self.validated_data['comment']
        print(comment_text)
        comment = Comment(comment=comment_text, user=kwargs['user'], blog=kwargs['blog'])
        comment.save()
        return comment


class CommentSerializer(serializers.ModelSerializer):

    blog = BlogSerializer(fields=('title', 'slug', 'community', 'date_updated'))

    # Custom Serializer Fields
    community = serializers.SerializerMethodField()
    community_image = serializers.SerializerMethodField()
    slug = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['pk', 'comment', 'timestamp', 'blog', 'community', 'community_image', 'slug']

    def validate_comment(self, comment):
        if len(comment) > 250:
            raise serializers.ValidationError("Maximum Comment length exceeded")
        return comment

    def get_community(self, obj):
        return obj.blog.community.name

    def get_community_image(self, obj):
        return obj.blog.community.avatarimage.url

    def get_slug(self, obj):
        return obj.blog.community.slug


class CommentBlogSerializer(serializers.ModelSerializer):

    user = AccountSerializer(fields=('first_name', 'last_name', 'profile_image', 'pk'))

    class Meta:
        model = Comment
        fields = ['pk', 'comment', 'timestamp', 'user']


class ReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = References
        fields = ['pk', 'refers', 'description']

# TODO -Tagged Blogs Personal Library Put On Halt
# class TaggedBlogCollectionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = TaggedBlogsCollection
#         fields = ['pk', 'collection_name', 'slug']


class TaggedBlogSerializer(serializers.ModelSerializer):
    blog = BlogSerializer(fields=('title', 'slug', 'description', 'community', 'date_updated',
                                  'image', 'vote_count', 'view_count', 'vote', 'comment_count'))

    class Meta:
        model = TaggedBlogs
        fields = ['pk', 'blog']

from rest_framework import serializers
from blog.models import Blog
from communities.models import Communities
from account.models import Account


class CommonsBlogSerializer(serializers.ModelSerializer):

    class Meta:
        model = Blog
        fields = ['title', 'slug']


class CommonsCommunitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Communities
        fields = ['slug', 'name', 'avatarimage']


class CommonsAccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ['first_name', 'last_name']

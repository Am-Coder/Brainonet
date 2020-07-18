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


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

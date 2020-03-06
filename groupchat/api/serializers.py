from rest_framework import serializers
from groupchat.models import Message


class MessageSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.first_name', read_only=True)
    community = serializers.CharField(source='community.name', read_only=True)

    class Meta:
        model = Message
        fields = '__all__'


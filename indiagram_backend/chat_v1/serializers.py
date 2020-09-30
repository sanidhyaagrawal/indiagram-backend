from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .models import MessageModel
from rest_framework.serializers import ModelSerializer, CharField


class MessageModelSerializer(ModelSerializer):
    user = CharField(source='user.username', read_only=True)
    recipient = CharField(source='recipient.username')

    class Meta:
        model = MessageModel
        fields = ('id', 'user', 'recipient', 'timestamp', 'body', 'seen', 'liked')


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)


from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import *


class loginSerializer(serializers.ModelSerializer):

    class Meta:
        model = user_details
        fields = ('key', 'username')


class username_suggestionsSerializer(serializers.ModelSerializer):
    response = serializers.CharField(max_length=200)
    suggestions = serializers.CharField(max_length=500)

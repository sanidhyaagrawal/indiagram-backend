
from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import *


class loginSerializer(serializers.ModelSerializer):
    class Meta:
        model = user_details
        fields = ('key', 'username')

class tokenised_contact_infoSerializer(serializers.ModelSerializer):
    class Meta:
        model = tokenised_contact_info
        fields = ('key', 'country_code', 'phone_number', 'email')


class user_detailsSerializer(serializers.ModelSerializer):
    date_of_birth = serializers.DateTimeField(format="%d-%m-%Y")

    class Meta:
        model = user_details
        fields = '__all__'


class username_suggestionsSerializer(serializers.ModelSerializer):
    response = serializers.CharField(max_length=200)
    suggestions = serializers.CharField(max_length=500)

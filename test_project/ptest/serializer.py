from django.contrib.auth.models import User,Group
from rest_framework import serializers
from .models import ReturnMessage
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        models = User
        fields = {'url','data_joined','username','email','group'}

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        models = Group
        fields = {'url','name'}
class MessageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        models = ReturnMessage
        fields = {'url','rcode','rmsg','data'}

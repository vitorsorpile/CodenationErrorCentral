from rest_framework import serializers

from login.models import User
from errors.models import Error

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password']

class ErrorSerializer(serializers.ModelSerializer):
    
    email = serializers.SerializerMethodField('get_user_email')
    
    class Meta:
        model = Error
        fields = [
            'id', 'title', 'category', 'level', 'archived',
            'description', 'address', 'date', 'events', 'email']

    def get_user_email(self, error):
        return error.user.email

class SimpleErrorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Error
        fields = [
            'id', 'title', 'category', 'level',
            'address', 'date', 'events'
        ]
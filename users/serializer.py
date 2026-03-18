from rest_framework import serializers
from .models import User

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

        fields = ['username', 'email', 'password', 'phone', 'role']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
class UserViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

        fields = ['id','username', 'email', 'phone', 'role']
from rest_framework import serializers
from .models import User, Pets, Shelter, AdoptionInquiry


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=true)

    class meta:
        model = User
        fields = ("id", "username", "email")

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"], email=validated_data
        )

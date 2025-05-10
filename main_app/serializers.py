from rest_framework import serializers
from .models import User, Pets, Shelter, Adoption_inquiry


class UserSerializer(serializers.ModelSerializer):
    password = serializers.char

    class meta:
        model = User
        fields = "__all__"

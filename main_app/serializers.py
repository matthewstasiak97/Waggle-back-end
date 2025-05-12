from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Pet, Shelter, AdoptionInquiry


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "password", "email"]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )

        return user


class ShelterSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Shelter
        fields = "__all__"


class PetSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    shelter = ShelterSerializer(read_only=True)

    class Meta:
        model = Pet
        fields = "__all__"


class AdoptionInquirySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    pet = PetSerializer(read_only=True)

    class Meta:
        model = AdoptionInquiry
        fields = "__all__"

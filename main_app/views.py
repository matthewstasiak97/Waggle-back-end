from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import generics, status, permissions, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Shelter, Pet, AdoptionInquiry
from .serializers import (
    UserSerializer,
    PetSerializer,
    ShelterSerializer,
    AdoptionInquirySerializer,
    PetSerializer,
)


class Home(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response({"message": "Welcome to the Waggle API!"})


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = User.objects.get(username=response.data["username"])
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": response.data,
            },
        )


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if not user:
            return Response(
                {"error": "Invalid credentials"},
            )

        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": UserSerializer(user).data,
            }
        )


class VerifyUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": UserSerializer(user).data,
            }
        )


class PetList(generics.ListCreateAPIView):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        try:
            shelter = self.request.user.shelter_profile
        except AttributeError:
            raise serializers.ValidationError(
                "Logged-in user does not have a shelter profile."
            )
        serializer.save(shelter=shelter)


class PetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer
    lookup_field = "id"

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]


class InquiryListCreate(generics.ListCreateAPIView):
    serializer_class = AdoptionInquirySerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        pet_id = self.kwargs["pet_id"]
        return AdoptionInquiry.objects.filter(pet_id=pet_id)

    def perform_create(self, serializer):
        pet = Pet.objects.get(id=self.kwargs["pet_id"])
        serializer.save(user=self.request.user, pet=pet)


class InquiryDetail(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = AdoptionInquirySerializer
    lookup_field = "id"
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        pet_id = self.kwargs["pet_id"]
        return AdoptionInquiry.objects.filter(pet_id=pet_id)


class ShelterList(generics.ListCreateAPIView):

    queryset = Shelter.objects.all()
    serializer_class = ShelterSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ShelterDetail(generics.RetrieveUpdateDestroyAPIView):

    queryset = Shelter.objects.all()
    serializer_class = ShelterSerializer
    lookup_field = "id"
    permission_classes = [permissions.IsAuthenticated]

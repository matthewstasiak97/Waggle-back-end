from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import generics, status, permissions, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Shelter, Pet, AdoptionInquiry
from .serializers import (
    UserSerializer,
    PetSerializer,
    ShelterSerializer,
    AdoptionInquirySerializer,
    PetSerializer,
)

def get_user_shelter_data(user):
    try:
        shelter = user.shelter_profile  # assuming OneToOneField with related_name='shelter_profile'
        return ShelterSerializer(shelter).data
    except Shelter.DoesNotExist:
        return None

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

        if request.data.get("is_shelter_owner"):
            shelter_name = request.data.get("shelter_name")
            shelter_location = request.data.get("shelter_location")

            if not shelter_name or not shelter_location:
                return Response(
                    {"error": "Shelter name and location are required."}, status=400
                )

            Shelter.objects.create(
                user=user,
                name=shelter_name,
                location=shelter_location,
                email=user.email,
                phone="",
            )

        shelter_data = get_user_shelter_data(user)
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": response.data,
                "shelter": shelter_data
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
                status=status.HTTP_400_BAD_REQUEST,
            )

        shelter_data = get_user_shelter_data(user)
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": UserSerializer(user).data,
                "shelter": shelter_data
            }
        )


class VerifyUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        shelter_data = get_user_shelter_data(user)
        refresh = RefreshToken.for_user(user)
        
        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": UserSerializer(user).data,
                "shelter": shelter_data
            }
        )


class PetList(generics.ListCreateAPIView):
    # queryset = Pet.objects.all()
    serializer_class = PetSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]
    
    def get_queryset(self):
        queryset = Pet.objects.all()
        species = self.request.query_params.get("species")
        if species:
            queryset = queryset.filter(species__iexact=species)
        return queryset

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

    def patch(self, request, *args, **kwargs):
        inquiry = self.get_object()
        pet = inquiry.pet

        if (
            not hasattr(request.user, "shelter_profile")
            or pet.shelter.user != request.user
        ):
            return Response(
                {"detail": "You do not have permission to modify this inquiry."},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Proceed with the update
        new_status = request.data.get("status")
        if new_status != "Accepted":
            return super().patch(
                request, *args, **kwargs
            )  # Allow other updates normally

        # Accepting the inquiry
        # Update the inquiry's status to Accepted
        inquiry.status = "Accepted"
        inquiry.save()

        # Update the Pet to reflect adoption
        pet.user = inquiry.user
        pet.is_adopted = True
        pet.save()

        # Deny all other pending inquiries for this pet
        AdoptionInquiry.objects.filter(pet=pet, status="Pending").exclude(
            id=inquiry.id
        ).update(status="Denied")

        # Serialize and return the updated inquiry
        serializer = self.get_serializer(inquiry)
        return Response(serializer.data, status=status.HTTP_200_OK)


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

    def get_object(self):
        obj = super().get_object()
        if obj.user != self.request.user:
            raise PermissionDenied("You do not have permission to access this shelter.")
        return obj


class UserAdoptionsAndInquiries(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        adopted_pets = Pet.objects.filter(user=user)
        user_inquiries = AdoptionInquiry.objects.filter(user=user)

        adopted_pets_data = PetSerializer(adopted_pets, many=True).data
        inquiries_data = AdoptionInquirySerializer(user_inquiries, many=True).data

        return Response({
            "adopted_pets": adopted_pets_data,
            "inquiries": inquiries_data
        })
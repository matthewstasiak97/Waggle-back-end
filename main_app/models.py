from django.db import models
from django.contrib.auth.models import (
    User,
)

SPECIES_CHOICES = [
    ("dog", "Dog"),
    ("cat", "Cat"),
]

APOPTION_CHOICES = [
    ("Pending", "Pending"),
    ("Accepted", "Accepted"),
    ("Denied", "Denied"),
]


class Shelter(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="shelter_profile"
    )

    def __str__(self):
        return f"{self.name} is owned by {self.user.username}"


class Pet(models.Model):
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=10, choices=SPECIES_CHOICES)
    breed = models.CharField(max_length=100, blank=True)
    age = models.PositiveIntegerField()
    description = models.TextField()
    image_url = models.URLField(blank=True)
    shelter = models.ForeignKey(Shelter, on_delete=models.CASCADE, related_name="pets")
    is_adopted = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.breed})"


class AdoptionInquiry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    prior_experience = models.BooleanField()
    currently_own_pet = models.BooleanField()
    status = models.CharField(
        max_length=20, default="Pending", choices=APOPTION_CHOICES
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Inquiry by {self.user.username} for {self.pet.name}"

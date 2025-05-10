from django.db import models
from django.contrib.auth.models import User

SPECIES_CHOICES = [
    ('dog', 'Dog'),
    ('cat', 'Cat'),
]




class Shelter(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    def __str__(self):
        return self.name
    
class User(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    def __str__(self):
        return self.name
    

class Pet(models.Model):
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=10, choices=SPECIES_CHOICES)
    breed = models.CharField(max_length=100, blank=True)
    age = models.PositiveIntegerField()
    description = models.TextField()
    image_url = models.URLField(blank=True)
    shelter = models.ForeignKey(Shelter, on_delete=models.CASCADE, related_name='pets')
    is_adopted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.breed})"


class AdoptionInquiry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    message = models.TextField()
    status = models.CharField(max_length=20, default='Pending') 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Inquiry by {self.user.username} for {self.pet.name}"
    
    
    
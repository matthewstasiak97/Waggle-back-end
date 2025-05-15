from django.contrib import admin
from .models import Shelter, Pet, AdoptionInquiry

# Register your models here.
admin.site.register(Shelter)
admin.site.register(Pet)
admin.site.register(AdoptionInquiry)

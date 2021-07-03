from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.
class PokemonEntry(models.Model):
    name = models.CharField(max_length=100) 
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    favorite = models.BooleanField()
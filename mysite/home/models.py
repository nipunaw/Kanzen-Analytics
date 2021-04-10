from django.db import models

# Create your models here.

class Anime(models.Model):
    anime_name = models.CharField(max_length=75, unique=True, primary_key=True)

    def __str__(self):
        return self.anime_name


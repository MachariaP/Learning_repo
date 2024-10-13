from django.db import models

# Create your models here.
class Profile(models.Model):
    name: models.CharField(max_length=100)
    phone_number: models.CharField(max_length=15)
    email: models.EmailField()
    degree: models.CharField(max_length=100)
    skills: models.TextField()
    about: models.TextField()

    def __str__(self):
        return self.name
    

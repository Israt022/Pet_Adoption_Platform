from django.db import models
from users.models import User
from pet.validators import validate_file_size
from cloudinary.models import CloudinaryField
# Create your models here.

class Pet(models.Model):
    DOG = 'dog'
    CAT = 'cat'
    BIRD = 'bird'
    OTHER = 'other'
    
    CATEGORY_CHOICES = [
        (DOG,'Dog'),
        (CAT,'Cat'),
        (BIRD,'Bird'),
        (OTHER,'Other'),
    ]

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=10,choices=CATEGORY_CHOICES)
    breed = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    description = models.TextField()
    availability = models.BooleanField(default=True)
    cost = models.DecimalField(max_digits=10,decimal_places=2,default=0.0)
    created_by = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name='add_pets')
    
    def __str__(self):
        return self.name
    
class PetImage(models.Model):
    pet = models.ForeignKey(
        Pet, on_delete=models.CASCADE, related_name='images')
    image = CloudinaryField('image')
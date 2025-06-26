from django.db import models
from django.contrib.auth.models import AbstractUser
from users.managers import CustomUserManager
from cloudinary.models import CloudinaryField
# Create your models here.

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    address = models.TextField(blank=True,null=True)
    phone_number = models.CharField(max_length=15,blank=True,null=True)
    balance = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    
    # Profile picture field
    profile_pic = CloudinaryField(
        'image',
        default='profile_pics/default',  
        blank=True,
        null=True
    )
    
    USERNAME_FIELD = 'email' # Use Email Instead of Username 
    REQUIRED_FIELDS = []
    
    objects = CustomUserManager()
    
    def __str__(self):
        return self.email
    
    
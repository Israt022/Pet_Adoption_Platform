from django.db import models
from django.contrib.auth.models import AbstractUser
from users.managers import CustomUserManager
# Create your models here.

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    address = models.TextField(blank=True,null=True)
    phone_number = models.CharField(max_length=15,blank=True,null=True)
    balance = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    
    # Profile picture field
    profile_pic = models.ImageField(
        upload_to='profile_pics/', 
        blank=True, 
        null=True, 
        default='profile_pics/default.png'
    )
    
    USERNAME_FIELD = 'email' # Use Email Instead of Username 
    REQUIRED_FIELDS = []
    
    objects = CustomUserManager()
    
    def __str__(self):
        return self.email
    
    
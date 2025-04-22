from django.db import models
from users.models import User
from pet.models import Pet
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
# Create your models here.

class Adoption(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='adoptions')
    pet = models.ForeignKey(Pet,on_delete=models.CASCADE,related_name='adoption')
    adoption_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.user.email} adopted {self.pet.name}'
    
class Deposite(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='deposits')
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.user.email} Deposite {self.amount}'
    

class Review(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE,related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ratings = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Review by {self.user.first_name} on {self.pet.name}"
    
class Payment(models.Model):
    PENDING = 'pending'
    COMPLETE = 'complete'
    FAILED = 'failed'
   
    STATUS_CHOICES = [
        (PENDING,'Pending'),
        (COMPLETE,'Complete'),
        (FAILED,'Failed'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,related_name='payments')
    adoption = models.OneToOneField('Adoption',on_delete=models.CASCADE,related_name='payment')
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    status = models.CharField(max_length=10,choices=STATUS_CHOICES,default='pending')
    transaction_id = models.CharField(max_length=100,blank=True,null = True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Payment {self.id} - {self.status}'
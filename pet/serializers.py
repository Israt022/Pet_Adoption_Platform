from rest_framework import serializers
from pet.models import Pet,PetImage
from users.serializers import UserSerializer

class PetImageSerializer(serializers.ModelSerializer):
    # image = serializers.ImageField()
    image = serializers.CharField(source='image.url')
    class Meta:
        model = PetImage
        fields = ['id', 'image']

class PetSerializers(serializers.ModelSerializer):
    created_by = UserSerializer(read_only = True)
    images = PetImageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Pet
        fields = ['id','name', 'category', 'breed', 'age', 'description','created_by',  'availability','images','cost']
        
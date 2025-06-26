from rest_framework import serializers
from adoption.models import Adoption,Deposite,Review
# from pet.serializers import PetSerializers
# from users.serializers import UserSerializer
from django.contrib.auth import get_user_model
from pet.models import Pet

class PetAdoptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = ['id','name','category','breed','cost','availability']

class AdoptionSerializer(serializers.ModelSerializer):
    # user = UserSerializer(read_only = True)
    pet_id = serializers.PrimaryKeyRelatedField(queryset=Pet.objects.filter(availability=True), write_only=True)
    pet = PetAdoptionSerializer(read_only=True)
    user = serializers.StringRelatedField(read_only = True)
    
    class Meta:
        model = Adoption
        fields = ['id','user','pet','pet_id','adoption_date']
    
class CreateAdoptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adoption
        fields = ['pet']
        
class DepositeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deposite
        fields = ['id','user','amount','date']
        read_only_fields = ['user','date']
     

class SimpleUserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(
        method_name='get_current_user_name')

    class Meta:
        model = get_user_model()
        fields = ['id', 'name']

    def get_current_user_name(self, obj):
        return obj.get_full_name()

   
class ReviewSerializer(serializers.ModelSerializer):
    # user = SimpleUserSerializer()
    user = serializers.SerializerMethodField(method_name='get_user')

    class Meta:
        model = Review
        fields = ['id', 'user', 'pet', 'ratings', 'comment']
        read_only_fields = ['user', 'pet']

    def get_user(self, obj):
        return SimpleUserSerializer(obj.user).data

    def validate(self, attrs):
        pet_id = self.context.get('pet_id')
        user = self.context['request'].user
        
        if not Adoption.objects.filter(user = user,pet_id = pet_id).exists():
            raise serializers.ValidationError('You can only review pet you have adopted.')
        return attrs
    
    # def create(self, validated_data):
    #     pet_id = self.context['pet_id']
    #     return Review.objects.create(pet_id=pet_id,user = self.context['request'].user, **validated_data)
    def create(self, validated_data):
        pet_id = self.context['pet_id']
        # Remove user from validated_data if present to avoid duplication
        validated_data.pop('user', None) 
        return Review.objects.create(pet_id=pet_id, user=self.context['request'].user, **validated_data)

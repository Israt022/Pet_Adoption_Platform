from djoser.serializers import UserCreateSerializer  as BaseUserCreateSerializer,UserSerializer as BaseUserSerializer
from rest_framework import serializers
from adoption.models import Adoption
from adoption.serializers import AdoptionSerializer
from users.models import User

class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id','email','password','first_name','last_name','address','phone_number','balance','profile_pic']
    

class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        ref_name = 'CustomUser'
        fields = ['id','email','first_name','last_name','address','phone_number','balance','profile_pic']
    
class AdoptionHistorySerializer(serializers.ModelSerializer):
    pet = serializers.SerializerMethodField()
    
    class Meta:
        model = Adoption
        fields = ['pet','adoption_date']
    
    def get_pet(self,obj):
        return {
            'name' : obj.pet.name,
            'category' : obj.pet.category
        }
    
                                     
    
    
class CustomerProfileSerializer(serializers.ModelSerializer):
    adoption_history = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id','email','first_name','last_name','address','phone_number','balance','adoption_history']
        read_only_fields = [
            'id', 'email', 'adoption_history','balance'
        ]
    def get_adoption_history(self,obj):
        adoptions = obj.adoptions.all()
        return AdoptionHistorySerializer(adoptions,many=True).data
    
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

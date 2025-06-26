from djoser.serializers import UserCreateSerializer  as BaseUserCreateSerializer,UserSerializer as BaseUserSerializer
from rest_framework import serializers
from adoption.models import Adoption
from adoption.serializers import AdoptionSerializer
from users.models import User

class UserCreateSerializer(BaseUserCreateSerializer):
    profile_pic = serializers.ImageField(required=False, allow_null=True)
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id','email','password','first_name','last_name','address','phone_number','balance','profile_pic']
    

class UserSerializer(BaseUserSerializer):
    profile_pic_url = serializers.SerializerMethodField()

    class Meta(BaseUserSerializer.Meta):
        ref_name = 'CustomUser'
        fields = ['id','email','first_name','last_name','address','phone_number','balance','profile_pic_url','is_staff']
        
        read_only_fields = ['is_staff']
    
    def get_profile_pic_url(self, obj):
        if obj.profile_pic:
            return obj.profile_pic.url
        return None
    
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
    profile_pic = serializers.ImageField(required=False, allow_null=True)
    
    class Meta:
        model = User
        fields = ['id','email','first_name','last_name','address','phone_number','balance','profile_pic','adoption_history']
        read_only_fields = [
            'id', 'email', 'adoption_history','balance'
        ]
    def get_adoption_history(self,obj):
        adoptions = obj.adoptions.all()
        return AdoptionHistorySerializer(adoptions,many=True).data
    def update(self, instance, validated_data):
        profile_pic = validated_data.pop('profile_pic', None)
        print("Profile pic in update:", profile_pic, type(profile_pic))

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if profile_pic is not None:
            instance.profile_pic = profile_pic

        instance.save()
        return instance


    
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

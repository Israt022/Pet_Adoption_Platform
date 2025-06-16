from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from users.serializers import CustomerProfileSerializer,ChangePasswordSerializer
from users.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
# Create your views here.
class CustomProfileViewSet(ModelViewSet):
    serializer_class = CustomerProfileSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'put', 'patch', 'delete']
    parser_classes = [MultiPartParser, FormParser]  # Important

    def get_queryset(self):
        return User.objects.filter(id = self.request.user.id)
    
    def get_object(self):
        return self.request.user
    
class ChangePasswordViewSet(ModelViewSet):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['post']
   
    def create(self,request,*args, **kwargs):
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        
        if not old_password or not new_password:
            return Response({'error': 'Old and new passwords are required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not user.check_password(old_password):
            return Response({'error': 'Incorrect old password.'}, status=status.HTTP_400_BAD_REQUEST)
        
        
        user.set_password(new_password)
        user.save()
        
        return Response({'message': 'Password updated successfully.'}, status=status.HTTP_200_OK)
        
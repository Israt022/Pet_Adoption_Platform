from django.shortcuts import render
from pet.serializers import PetSerializers,PetImageSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated,SAFE_METHODS,IsAdminUser,AllowAny
from pet.models import Pet,PetImage
from django_filters.rest_framework import DjangoFilterBackend
from api.permissions import IsAdminOrReadOnly
from drf_yasg.utils import swagger_auto_schema
from pet.paginations import DefaultPagination
# Create your views here.

class PetViewSet(ModelViewSet):
    """
    API endpoint for managing pet in the e-commerce store
     - Allows authenticated admin to create, update, and delete pet
     - Allows users to browse and filter pet
     - Support ordering by price and updated_at
    """
    
    queryset = Pet.objects.all()
    serializer_class = PetSerializers
    
    filter_backends = [DjangoFilterBackend]
    pagination_class = DefaultPagination
    filterset_fields = ['category']
    
    def get_permissions(self):
        if self.action in ['list','retrive']:
            return [AllowAny()]
        if self.action == 'create':
            return [IsAuthenticated()]
        if self.action in ['update','partial_update','destroy']:
            return [IsAdminUser()]
        return super().get_permissions()
    @swagger_auto_schema(tags=['Pets'])
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
       
    @swagger_auto_schema(tags=['Pets'])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Pets'])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Pets'])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Pets'])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Pets'])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Pets'])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)   
       
     
class PetImageViewSet(ModelViewSet):
    serializer_class = PetImageSerializer
    # permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        return PetImage.objects.filter(pet_id=self.kwargs.get('pet_pk'))
    def get_permissions(self):
        if self.action in ['list','retrive']:
            return [AllowAny()]
        if self.action == 'create':
            return [IsAuthenticated()]
        if self.action in ['update','partial_update','destroy']:
            return [IsAdminUser()]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(pet_id=self.kwargs.get('pet_pk'))
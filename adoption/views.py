from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from adoption.models import Adoption,Deposite,Review
from adoption.serializers import AdoptionSerializer,DepositeSerializer,ReviewSerializer
from adoption.permissions import IsReviewAuthorOrReadonly,IsCustomer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from pet.models import Pet
from pet.serializers import PetSerializers

# Create your views here.
class AdoptionViewSet(ModelViewSet):
    queryset = Adoption.objects.all()
    serializer_class = AdoptionSerializer
    # permission_classes = [IsAuthenticated,IsCustomer]
    
    def create(self, request, *args, **kwargs):
        pet_id = request.data.get('pet_id')
        if request.user.is_staff:
            return Response({'error': 'Admin cannot adopt pets.'}, status=status.HTTP_403_FORBIDDEN)
        if not pet_id:
            return Response({'error': 'Pet ID is required.'},status = status.HTTP_400_BAD_REQUEST)
        
        try:
            pet = Pet.objects.get(id=pet_id)
        except Pet.DoesNotExist:
            return Response({'error' : 'Pet not found.'},status = status.HTTP_404_NOT_FOUND)
        
        if not  pet.availability:
            return Response({'error':'Pet is not available for adoption.'},status=status.HTTP_400_BAD_REQUEST)
        
        user = request.user
        
        if user.balance < pet.cost:
            return Response({'error' : 'Insufficient balance.'},status=status.HTTP_400_BAD_REQUEST)
        
        user.balance -= pet.cost
        user.save()
        
        pet.availability = False
        pet.save()
        
        adoption = Adoption.objects.create(user = user,pet = pet)
        
        serializer = self.get_serializer(adoption)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    
    def get_permissions(self):
        if self.action == 'create':
            return [IsCustomer()]
        elif self.action in ['list','retrieve']:
            return [IsAuthenticated()]
        else:
            return[IsAdminUser()]
        
        
class DepositeViewSet(ModelViewSet):
    # queryset = Pet.objects.all()
    serializer_class = DepositeSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post']
    
    def get_queryset(self):
        return Deposite.objects.filter(user = self.request.user)
   
    def perform_create(self, serializer):
        deposit = serializer.save(user=self.request.user)
        # update user balance
        user = self.request.user
        user.balance += deposit.amount
        user.save()
    

class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewAuthorOrReadonly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Review.objects.filter(pet_id=self.kwargs.get('pet_pk'))

    def get_serializer_context(self):
        return {'pet_id': self.kwargs.get('pet_pk')}

class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewAuthorOrReadonly]
    def get_queryset(self):
        return Review.objects.filter(pet_id=self.kwargs.get('pet_pk'))

    def get_serializer_context(self):
        return {'pet_id': self.kwargs.get('pet_pk'),'request' : self.request}

from rest_framework import permissions
from adoption.models import Adoption

class IsReviewAuthorOrReadonly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if not request.user or not request.user.is_authenticated or request.user.is_staff:
            return False
        
        pet_id = view.kwargs.get('pet_pk')
        return Adoption.objects.filter(user=request.user, pet_id=pet_id).exists()
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        # if request.user.is_staff:
        #     return True

        return obj.user == request.user
    
class IsCustomer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and not request.user.is_staff
            
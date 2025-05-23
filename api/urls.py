from django.urls import path,include
from rest_framework_nested import routers
from pet.views import PetViewSet,PetImageViewSet
from adoption.views import ReviewViewSet,AdoptionViewSet,DepositeViewSet
from users.views import CustomProfileViewSet,ChangePasswordViewSet


router = routers.DefaultRouter()
router.register('pets',PetViewSet,basename='pets')
router.register('deposits', DepositeViewSet, basename='deposits')
router.register('adoptions',AdoptionViewSet,basename='adoptions')
router.register('profile',CustomProfileViewSet,basename='profile')
router.register('change-password',ChangePasswordViewSet,basename='change-password')

pet_router = routers.NestedDefaultRouter(
    router, 'pets', lookup='pet')
pet_router.register('reviews', ReviewViewSet, basename='pet-review')
pet_router.register('images', PetImageViewSet,
                        basename='pet-images')


# pet_router = routers.NestedDefaultRouter(router,'pets',lookup='pet')
# pet_router.
urlpatterns = [
    path('', include(router.urls)),
    path('', include(pet_router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]

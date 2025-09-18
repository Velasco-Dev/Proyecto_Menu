from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PlatoViewSet
from .views import IngredientesViewSet

router = DefaultRouter()
router.register(r'platos', PlatoViewSet)
router.register(r'ingredientes', IngredientesViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
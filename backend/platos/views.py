from rest_framework import viewsets
from .models import Plato, Ingrediente
from .serializers import PlatoSerializer, IngredienteSerializer

class PlatoViewSet(viewsets.ModelViewSet):
    queryset = Plato.objects.all()
    serializer_class = PlatoSerializer
    
class IngredientesViewSet(viewsets.ModelViewSet):
    queryset = Ingrediente.objects.all()
    serializer_class = IngredienteSerializer

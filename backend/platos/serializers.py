from rest_framework import serializers
from .models import Plato, Ingrediente

class IngredienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingrediente
        fields = ['id', 'nombre', 'icono', 'puntuacion', 'seleccionado']

class PlatoSerializer(serializers.ModelSerializer):
    ingredientes = IngredienteSerializer(many=True, read_only=True)
    ingredientes_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Ingrediente.objects.all(), write_only=True, source='ingredientes'
    )

    class Meta:
        model = Plato
        fields = ['id', 'nombre', 'imagen', 'descripcion', 'puntuacion', 'precio', 'ingredientes', 'ingredientes_ids']
from rest_framework import viewsets
from .models import Plato, Ingrediente
from .serializers import PlatoSerializer, IngredienteSerializer
from platos.algoritmos.listaDoblementeEnlazada import ListaDoblementeEnlazada

from rest_framework.decorators import api_view
from rest_framework.response import Response

class PlatoViewSet(viewsets.ModelViewSet):
    queryset = Plato.objects.all()
    serializer_class = PlatoSerializer
    
class IngredientesViewSet(viewsets.ModelViewSet):
    queryset = Ingrediente.objects.all()
    serializer_class = IngredienteSerializer

@api_view(['GET'])
def platos_ordenados_view(request):
    lista = ListaDoblementeEnlazada()
    platos = Plato.objects.prefetch_related('ingredientes').all()
    for plato in platos:
        ingredientes_seleccionados = [
            ing for ing in plato.ingredientes.all() if ing.seleccionado
        ]
        if ingredientes_seleccionados:  # Solo platos con ingredientes seleccionados
            puntuacion_total = round(
                                    sum(ing.puntuacion for ing in ingredientes_seleccionados) / len(ingredientes_seleccionados), 2
                                )
            plato_dict = {
                "id": plato.id,
                "nombre": plato.nombre,
                "descripcion": plato.descripcion,
                "imagen": plato.imagen,
                "precio": plato.precio,
                "ingredientes": [
                    {"nombre": ing.nombre, "icono": ing.icono, "puntuacion": ing.puntuacion}
                    for ing in ingredientes_seleccionados
                ],
                "puntuacion_total": puntuacion_total
            }
            lista.insertar_ordenado(plato_dict, puntuacion_total)
    lista.recorrerAdelante()
    # Recorrer la lista y devolver como JSON
    platos_ordenados = []
    actual = lista.cabeza
    while actual:
        platos_ordenados.append(actual.plato)
        actual = actual.siguiente
    return Response(platos_ordenados)

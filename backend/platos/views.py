from rest_framework import viewsets
from .models import Plato, Ingrediente
from .serializers import PlatoSerializer, IngredienteSerializer
from platos.algoritmos.listaDoblementeEnlazada import ListaDoblementeEnlazada
from platos.algoritmos.arbolDecisionSmartMeal import arbol_smart_meal

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

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
            puntuacion_total = sum(ing.puntuacion for ing in ingredientes_seleccionados)
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
    # Recorrer la lista y devolver como JSON
    platos_ordenados = []
    actual = lista.cabeza
    while actual:
        platos_ordenados.append(actual.plato)
        actual = actual.siguiente
    return Response(platos_ordenados)


# ========================================
# VISTAS PARA EL ÁRBOL DE DECISIÓN SMARTMEAL
# ========================================

@api_view(['GET'])
def smartmeal_inicio(request):
    """
    Vista para obtener el nodo inicial del árbol SmartMeal.
    
    Retorna:
        - Pregunta inicial sobre tipo de comida
        - Opciones disponibles (Desayuno, Almuerzo, Cena)
    """
    try:
        navegacion = arbol_smart_meal.navegar_a('inicio')
        if navegacion:
            return Response(navegacion)
        else:
            return Response(
                {'error': 'No se pudo inicializar SmartMeal'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    except Exception as e:
        return Response(
            {'error': f'Error interno: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def smartmeal_navegar(request, id_nodo):
    """
    Vista para navegar a un nodo específico del árbol SmartMeal.
    
    Args:
        id_nodo (str): ID del nodo al que se quiere navegar
    
    Retorna:
        - Información del nodo actual
        - Opciones disponibles desde ese nodo
        - Ruta completa hasta el nodo
        - Si es un resultado final o no
    """
    try:
        navegacion = arbol_smart_meal.navegar_a(id_nodo)
        if navegacion:
            return Response(navegacion)
        else:
            return Response(
                {'error': f'Nodo "{id_nodo}" no encontrado'}, 
                status=status.HTTP_404_NOT_FOUND
            )
    except Exception as e:
        return Response(
            {'error': f'Error al navegar: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def smartmeal_obtener_opciones(request, id_nodo):
    """
    Vista para obtener solo las opciones disponibles desde un nodo.
    
    Args:
        id_nodo (str): ID del nodo del cual obtener las opciones
    
    Retorna:
        - Lista de opciones disponibles
    """
    try:
        opciones = arbol_smart_meal.obtener_opciones(id_nodo)
        return Response({'opciones': opciones})
    except Exception as e:
        return Response(
            {'error': f'Error al obtener opciones: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def smartmeal_estructura_completa(request):
    """
    Vista para obtener la estructura completa del árbol (solo para debugging).
    
    ADVERTENCIA: Esta vista retorna mucha información y solo debería usarse
    para propósitos de desarrollo y debugging.
    """
    try:
        estructura = arbol_smart_meal.obtener_estructura_completa()
        return Response(estructura)
    except Exception as e:
        return Response(
            {'error': f'Error al obtener estructura: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
def smartmeal_buscar_platos_por_ingredientes(request):
    """
    Vista para buscar platos reales en la base de datos que coincidan
    con los ingredientes seleccionados en el árbol SmartMeal.
    
    Body esperado:
        {
            "ingredientes": ["pollo", "arroz", "ajo", "cebolla"]
        }
    
    Retorna:
        - Lista de platos que contienen esos ingredientes
        - Platos ordenados por cantidad de coincidencias
    """
    try:
        ingredientes_buscados = request.data.get('ingredientes', [])
        
        if not ingredientes_buscados:
            return Response(
                {'error': 'Debe proporcionar al menos un ingrediente'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Buscar platos que contengan los ingredientes especificados
        platos_coincidentes = []
        
        for plato in Plato.objects.prefetch_related('ingredientes').all():
            ingredientes_plato = [ing.nombre.lower() for ing in plato.ingredientes.all()]
            
            # Contar coincidencias (búsqueda parcial)
            coincidencias = 0
            for ing_buscado in ingredientes_buscados:
                for ing_plato in ingredientes_plato:
                    if ing_buscado.lower() in ing_plato or ing_plato in ing_buscado.lower():
                        coincidencias += 1
                        break
            
            if coincidencias > 0:
                plato_dict = {
                    "id": plato.id,
                    "nombre": plato.nombre,
                    "descripcion": plato.descripcion,
                    "imagen": plato.imagen,
                    "precio": float(plato.precio),
                    "puntuacion": plato.puntuacion,
                    "ingredientes": [
                        {
                            "nombre": ing.nombre, 
                            "icono": ing.icono, 
                            "puntuacion": ing.puntuacion
                        }
                        for ing in plato.ingredientes.all()
                    ],
                    "coincidencias": coincidencias,
                    "porcentaje_coincidencia": round((coincidencias / len(ingredientes_buscados)) * 100, 2)
                }
                platos_coincidentes.append(plato_dict)
        
        # Ordenar por cantidad de coincidencias (mayor a menor)
        platos_coincidentes.sort(key=lambda x: x['coincidencias'], reverse=True)
        
        return Response({
            'ingredientes_buscados': ingredientes_buscados,
            'total_platos_encontrados': len(platos_coincidentes),
            'platos': platos_coincidentes
        })
        
    except Exception as e:
        return Response(
            {'error': f'Error en la búsqueda: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

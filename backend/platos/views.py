from rest_framework import viewsets
from .models import Plato, Ingrediente
from .serializers import PlatoSerializer, IngredienteSerializer
from platos.algoritmos.listaDoblementeEnlazada import ListaDoblementeEnlazada
from platos.algoritmos.arbolDecisionSmartMeal import arbol_smart_meal

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone

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
    global arbol_smart_meal
    
    try:
        # Verificar que el árbol existe y está inicializado
        if not hasattr(arbol_smart_meal, 'raiz') or arbol_smart_meal.raiz is None:
            # Reinicializar el árbol si es necesario
            from platos.algoritmos.arbolDecisionSmartMeal import ArbolDecisionSmartMeal
            arbol_smart_meal = ArbolDecisionSmartMeal()
        
        navegacion = arbol_smart_meal.navegar_a('inicio')
        if navegacion:
            return Response({
                'success': True,
                'message': 'Menu Marta SmartMeal inicializado correctamente',
                **navegacion
            })
        else:
            return Response(
                {
                    'error': 'No se pudo inicializar Menu Marta SmartMeal',
                    'success': False,
                    'details': 'El árbol de decisión no está disponible'
                }, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    except ImportError as e:
        return Response(
            {
                'error': 'Error de configuración del sistema',
                'success': False,
                'details': f'No se pudo cargar el módulo SmartMeal: {str(e)}'
            }, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    except Exception as e:
        return Response(
            {
                'error': 'Error interno del servidor',
                'success': False, 
                'details': str(e)
            }, 
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
    global arbol_smart_meal
    
    try:
        # Validar que el ID del nodo no esté vacío
        if not id_nodo or not isinstance(id_nodo, str):
            return Response(
                {
                    'error': 'ID de nodo inválido',
                    'success': False,
                    'details': 'El ID del nodo debe ser una cadena válida'
                }, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Verificar que el árbol esté disponible
        if not hasattr(arbol_smart_meal, 'nodos') or not arbol_smart_meal.nodos:
            return Response(
                {
                    'error': 'Sistema SmartMeal no disponible',
                    'success': False,
                    'details': 'El árbol de decisión no está inicializado'
                }, 
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        
        navegacion = arbol_smart_meal.navegar_a(id_nodo)
        if navegacion:
            return Response({
                'success': True,
                'message': f'Navegación exitosa al nodo: {id_nodo}',
                **navegacion
            })
        else:
            return Response(
                {
                    'error': f'Nodo "{id_nodo}" no encontrado en Menu Marta',
                    'success': False,
                    'details': f'El nodo solicitado no existe en el árbol de decisión',
                    'nodos_disponibles': list(arbol_smart_meal.nodos.keys())[:10]  # Primeros 10 para debugging
                }, 
                status=status.HTTP_404_NOT_FOUND
            )
    except AttributeError as e:
        return Response(
            {
                'error': 'Error de configuración interna',
                'success': False,
                'details': f'El sistema SmartMeal no está correctamente configurado: {str(e)}'
            }, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    except Exception as e:
        return Response(
            {
                'error': 'Error interno durante la navegación',
                'success': False, 
                'details': str(e)
            }, 
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
    global arbol_smart_meal
    
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
    global arbol_smart_meal
    
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
    Vista para buscar platos reales en la base de datos JSON que coincidan
    con los ingredientes seleccionados en el árbol SmartMeal.
    
    Body esperado:
        {
            "ingredientes": ["pollo", "arroz", "ajo", "cebolla"]
        }
    
    Retorna:
        - Lista de platos que contienen esos ingredientes
        - Platos ordenados por cantidad de coincidencias
    """
    import json
    import os
    
    try:
        ingredientes_buscados = request.data.get('ingredientes', [])
        
        if not ingredientes_buscados:
            return Response(
                {'error': 'Debe proporcionar al menos un ingrediente'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Cargar la base de datos de platos desde el archivo JSON
        json_path = os.path.join(os.path.dirname(__file__), '..', 'platos_database.json')
        
        try:
            with open(json_path, 'r', encoding='utf-8') as file:
                platos_db = json.load(file)
        except FileNotFoundError:
            return Response(
                {'error': 'Base de datos de platos no encontrada'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except json.JSONDecodeError:
            return Response(
                {'error': 'Error al leer la base de datos de platos'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        # Buscar platos que contengan los ingredientes especificados
        platos_coincidentes = []
        
        for plato in platos_db:
            if not plato.get('disponible', True):
                continue  # Saltar platos no disponibles
                
            ingredientes_plato = [ing.lower() for ing in plato.get('ingredientes', [])]
            
            # Contar coincidencias (búsqueda parcial y flexible)
            coincidencias = 0
            ingredientes_encontrados = []
            
            for ing_buscado in ingredientes_buscados:
                ing_buscado_lower = ing_buscado.lower().strip()
                for ing_plato in ingredientes_plato:
                    # Búsqueda flexible: coincidencia parcial en ambas direcciones
                    if (ing_buscado_lower in ing_plato or 
                        ing_plato in ing_buscado_lower or
                        any(palabra in ing_plato for palabra in ing_buscado_lower.split()) or
                        any(palabra in ing_buscado_lower for palabra in ing_plato.split())):
                        coincidencias += 1
                        ingredientes_encontrados.append(ing_plato)
                        break
            
            if coincidencias > 0:
                # Calcular score de relevancia
                score_relevancia = (coincidencias / len(ingredientes_buscados)) * plato.get('puntuacion', 4.0)
                
                plato_resultado = {
                    "id": plato["id"],
                    "nombre": plato["nombre"],
                    "descripcion": plato["descripcion"],
                    "categoria": plato.get("categoria", ""),
                    "tipo": plato.get("tipo", ""),
                    "imagen": plato.get("imagen", ""),
                    "precio": plato.get("precio", 0),
                    "puntuacion": plato.get("puntuacion", 4.0),
                    "tiempo_preparacion": plato.get("tiempo_preparacion", ""),
                    "calorias": plato.get("calorias", 0),
                    "ingredientes_coincidentes": ingredientes_encontrados,
                    "total_coincidencias": coincidencias,
                    "score_relevancia": round(score_relevancia, 2),
                    "ingredientes_completos": plato.get("ingredientes", []),
                    "porcentaje_coincidencia": round((coincidencias / len(ingredientes_buscados)) * 100, 2)
                }
                platos_coincidentes.append(plato_resultado)
        
        # Ordenar por score de relevancia (mayor a menor), luego por coincidencias
        platos_coincidentes.sort(key=lambda x: (x['score_relevancia'], x['total_coincidencias']), reverse=True)
        
        # Limitar resultados a los más relevantes (máximo 10)
        platos_coincidentes = platos_coincidentes[:10]
        
        return Response({
            'success': True,
            'message': f'Se encontraron {len(platos_coincidentes)} platos que coinciden con los ingredientes',
            'ingredientes_buscados': ingredientes_buscados,
            'total_platos_encontrados': len(platos_coincidentes),
            'platos': platos_coincidentes,
            'timestamp': timezone.now().isoformat()
        })
        
    except Exception as e:
        return Response(
            {'error': f'Error en la búsqueda: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def smartmeal_health_check(request):
    """
    Vista para verificar el estado del sistema SmartMeal.
    
    Retorna información sobre el estado del árbol y estadísticas básicas.
    """
    global arbol_smart_meal
    
    try:
        health_status = {
            'sistema': 'Menu Marta - SmartMeal',
            'status': 'OK',
            'timestamp': timezone.now().isoformat(),
        }
        
        # Verificar árbol de decisión
        if hasattr(arbol_smart_meal, 'raiz') and arbol_smart_meal.raiz:
            health_status['arbol_decision'] = {
                'status': 'Activo',
                'nodo_raiz': arbol_smart_meal.raiz.id_nodo,
                'total_nodos': len(arbol_smart_meal.nodos) if hasattr(arbol_smart_meal, 'nodos') else 0
            }
        else:
            health_status['arbol_decision'] = {
                'status': 'No inicializado',
                'error': 'El árbol de decisión no está disponible'
            }
            health_status['status'] = 'WARNING'
        
        # Verificar base de datos
        try:
            platos_count = Plato.objects.count()
            ingredientes_count = Ingrediente.objects.count()
            health_status['base_datos'] = {
                'status': 'Conectada',
                'platos': platos_count,
                'ingredientes': ingredientes_count
            }
        except Exception as db_error:
            health_status['base_datos'] = {
                'status': 'Error',
                'error': str(db_error)
            }
            health_status['status'] = 'ERROR'
        
        # Determinar código de estado HTTP
        if health_status['status'] == 'OK':
            return Response(health_status)
        elif health_status['status'] == 'WARNING':
            return Response(health_status, status=status.HTTP_206_PARTIAL_CONTENT)
        else:
            return Response(health_status, status=status.HTTP_503_SERVICE_UNAVAILABLE)
            
    except Exception as e:
        return Response(
            {
                'sistema': 'Menu Marta - SmartMeal',
                'status': 'ERROR',
                'error': 'Error crítico del sistema',
                'details': str(e),
                'timestamp': timezone.now().isoformat(),
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

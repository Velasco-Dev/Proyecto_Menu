from rest_framework import viewsets
from .models import Plato, Ingrediente
from .serializers import PlatoSerializer, IngredienteSerializer
from platos.algoritmos.listaDoblementeEnlazada import ListaDoblementeEnlazada
from platos.algoritmos.arbolDecisionSmartMeal import arbol_smart_meal
from platos.algoritmos.grafoBusquedaReceta import build_graph_desde_db

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone

import os
import json

# Variable global para cachear el grafo (evita reconstruirlo cada vez)
_grafo_cache = None
_timestamp_cache = None

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
    
"""
Vistas para búsqueda de recetas usando Grafo Bipartito Dirigido.
"""

def obtener_grafo():
    """
    Obtiene el grafo cacheado o lo construye si no existe.
    El caché se invalida si el archivo JSON es más reciente.
    """
    global _grafo_cache, _timestamp_cache
    
    json_path = os.path.join(os.path.dirname(__file__), '..', 'platos_database.json')
    
    # Verificar si el archivo existe
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"Base de datos de platos no encontrada en {json_path}")
    
    # Obtener timestamp del archivo
    file_timestamp = os.path.getmtime(json_path)
    
    # Si el caché existe y el archivo no ha cambiado, usar el caché
    if _grafo_cache is not None and _timestamp_cache == file_timestamp:
        print("[INFO] Usando grafo cacheado")
        return _grafo_cache
    
    # Cargar el archivo JSON
    print("[INFO] Construyendo nuevo grafo desde JSON...")
    with open(json_path, 'r', encoding='utf-8') as f:
        platos_db = json.load(f)
    
    # Construir el grafo
    grafo = build_graph_desde_db(platos_db)
    
    # Cachear el grafo
    _grafo_cache = grafo
    _timestamp_cache = file_timestamp
    
    return grafo


@api_view(['POST'])
def grafo_buscar_recetas(request):
    """
    Busca recetas basadas en ingredientes disponibles usando el Grafo Bipartito Dirigido.
    
    Body esperado:
        {
            "ingredientes": ["pollo", "arroz", "ajo"],
            "umbral_casi_completa": 0.75
        }
    
    Retorna:
        {
            "success": True,
            "ingredientes_buscados": [...],
            "resultados": {
                "completas": [...],
                "casi_completas": [...],
                "incompletas": [...]
            },
            "estadisticas": {
                "total_completas": 0,
                "total_casi_completas": 0,
                "total_incompletas": 0,
                "total_recetas": 0
            },
            "timestamp": "..."
        }
    """
    try:
        # Validar entrada
        ingredientes_buscados = request.data.get('ingredientes', [])
        umbral = request.data.get('umbral_casi_completa', 0.75)
        
        if not isinstance(ingredientes_buscados, list) or not ingredientes_buscados:
            return Response(
                {
                    'success': False,
                    'message': 'Se requiere una lista no vacía de ingredientes.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validar umbral
        if not (0 <= umbral <= 1):
            return Response(
                {
                    'success': False,
                    'message': 'El umbral debe estar entre 0 y 1.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Obtener el grafo
        grafo = obtener_grafo()
        
        # Buscar recetas
        print(f"[INFO] Buscando recetas con ingredientes: {ingredientes_buscados}")
        resultados = grafo.buscar_recetas_por_ingredientes(
            ingredientes_buscados,
            umbral_casi_completa=umbral
        )
        
        # Calcular estadísticas
        estadisticas = {
            'total_completas': len(resultados['completas']),
            'total_casi_completas': len(resultados['casi_completas']),
            'total_incompletas': len(resultados['incompletas']),
            'total_recetas': len(resultados['completas']) + len(resultados['casi_completas']) + len(resultados['incompletas'])
        }
        
        return Response({
            'success': True,
            'message': f'Se han encontrado {estadisticas["total_recetas"]} recetas',
            'ingredientes_buscados': ingredientes_buscados,
            'umbral_utilizado': umbral,
            'resultados': resultados,
            'estadisticas': estadisticas,
            'timestamp': timezone.now().isoformat()
        })
    
    except FileNotFoundError as e:
        return Response(
            {
                'success': False,
                'message': f'Base de datos no encontrada: {str(e)}'
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    except json.JSONDecodeError as e:
        return Response(
            {
                'success': False,
                'message': f'Error al parsear JSON: {str(e)}'
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    except Exception as e:
        print(f"[ERROR] {str(e)}")
        return Response(
            {
                'success': False,
                'message': f'Error interno: {str(e)}'
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def grafo_estadisticas(request):
    """
    Retorna estadísticas del grafo (cantidad de ingredientes, recetas, aristas).
    Útil para debugging y monitoreo.
    
    Retorna:
        {
            "success": True,
            "estadisticas": {
                "total_ingredientes": 0,
                "total_recetas": 0,
                "total_aristas": 0
            },
            "timestamp": "..."
        }
    """
    try:
        grafo = obtener_grafo()
        
        # Calcular total de aristas
        total_aristas = sum(len(v) for v in grafo.adyacencia.values())
        
        estadisticas = {
            'total_ingredientes': len(grafo.ingredientes),
            'total_recetas': len(grafo.recetas),
            'total_aristas': total_aristas
        }
        
        return Response({
            'success': True,
            'estadisticas': estadisticas,
            'timestamp': timezone.now().isoformat()
        })
    
    except Exception as e:
        return Response(
            {
                'success': False,
                'message': f'Error: {str(e)}'
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def grafo_ingredientes_disponibles(request):
    """
    Retorna la lista de todos los ingredientes disponibles en el grafo.
    Útil para el frontend para mostrar qué ingredientes se pueden seleccionar.
    
    Retorna:
        {
            "success": True,
            "ingredientes": ["pollo", "arroz", ...],
            "total": 0,
            "timestamp": "..."
        }
    """
    try:
        grafo = obtener_grafo()
        
        # Extraer nombres de ingredientes
        ingredientes = sorted([ing.get_name() for ing in grafo.ingredientes])
        
        return Response({
            'success': True,
            'ingredientes': ingredientes,
            'total': len(ingredientes),
            'timestamp': timezone.now().isoformat()
        })
    
    except Exception as e:
        return Response(
            {
                'success': False,
                'message': f'Error: {str(e)}'
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def grafo_recetas_disponibles(request):
    """
    Retorna la lista de todas las recetas disponibles en el grafo.
    
    Retorna:
        {
            "success": True,
            "recetas": ["Arroz con pollo", ...],
            "total": 0,
            "timestamp": "..."
        }
    """
    try:
        grafo = obtener_grafo()
        
        # Extraer nombres de recetas
        recetas = sorted([receta.get_name() for receta in grafo.recetas])
        
        return Response({
            'success': True,
            'recetas': recetas,
            'total': len(recetas),
            'timestamp': timezone.now().isoformat()
        })
    
    except Exception as e:
        return Response(
            {
                'success': False,
                'message': f'Error: {str(e)}'
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def grafo_health_check(request):
    """
    Verifica que el grafo esté disponible y funcional.
    
    Retorna:
        {
            "success": True,
            "message": "Grafo operativo",
            "timestamp": "..."
        }
    """
    try:
        grafo = obtener_grafo()
        
        if grafo is None or len(grafo.ingredientes) == 0 or len(grafo.recetas) == 0:
            return Response({
                'success': False,
                'message': 'Grafo no inicializado correctamente'
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        
        return Response({
            'success': True,
            'message': 'Grafo operativo',
            'timestamp': timezone.now().isoformat()
        })
    
    except Exception as e:
        return Response(
            {
                'success': False,
                'message': f'Error: {str(e)}'
            },
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )

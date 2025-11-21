from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PlatoViewSet, 
    IngredientesViewSet,
    platos_ordenados_view,
    smartmeal_inicio,
    smartmeal_navegar,
    smartmeal_obtener_opciones,
    smartmeal_estructura_completa,
    smartmeal_buscar_platos_por_ingredientes,
    smartmeal_health_check,
    grafo_buscar_recetas,
    grafo_estadisticas,
    grafo_ingredientes_disponibles,
    grafo_recetas_disponibles,
    grafo_health_check
)

router = DefaultRouter()
router.register(r'platos', PlatoViewSet)
router.register(r'ingredientes', IngredientesViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('platos-ordenados/', platos_ordenados_view, name='platos-ordenados'),
    
    # ========================================
    # RUTAS PARA EL ÁRBOL DE DECISIÓN SMARTMEAL
    # ========================================
    
    # Ruta inicial - obtiene la pregunta de inicio
    path('menu-arbol/', smartmeal_inicio, name='smartmeal-inicio'),
    
    # Navegación por ID de nodo
    path('menu-arbol/navegar/<str:id_nodo>/', smartmeal_navegar, name='smartmeal-navegar'),
    
    # Obtener solo opciones de un nodo
    path('menu-arbol/opciones/<str:id_nodo>/', smartmeal_obtener_opciones, name='smartmeal-opciones'),
    
    # Buscar platos reales por ingredientes del árbol
    path('menu-arbol/buscar-platos/', smartmeal_buscar_platos_por_ingredientes, name='smartmeal-buscar-platos'),
    
    # Verificación de salud del sistema
    path('menu-arbol/health/', smartmeal_health_check, name='smartmeal-health'),
    
    # Estructura completa (solo para debugging)
    path('menu-arbol/debug/estructura/', smartmeal_estructura_completa, name='smartmeal-debug'),

    #"""
    #URLs para las vistas del Grafo Bipartito Dirigido.
    #"""

    # Búsqueda principal de recetas por ingredientes
    path('grafo/buscar/', grafo_buscar_recetas, name='grafo-buscar'),
    
    # Estadísticas del grafo
    path('grafo/estadisticas/', grafo_estadisticas, name='grafo-estadisticas'),
    
    # Obtener ingredientes disponibles
    path('grafo/ingredientes/', grafo_ingredientes_disponibles, name='grafo-ingredientes'),
    
    # Obtener recetas disponibles
    path('grafo/recetas/', grafo_recetas_disponibles, name='grafo-recetas'),
    
    # Health check
    path('grafo/health/', grafo_health_check, name='grafo-health'),
]
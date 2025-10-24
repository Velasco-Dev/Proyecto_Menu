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
    smartmeal_buscar_platos_por_ingredientes
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
    path('smartmeal/', smartmeal_inicio, name='smartmeal-inicio'),
    
    # Navegación por ID de nodo
    path('smartmeal/navegar/<str:id_nodo>/', smartmeal_navegar, name='smartmeal-navegar'),
    
    # Obtener solo opciones de un nodo
    path('smartmeal/opciones/<str:id_nodo>/', smartmeal_obtener_opciones, name='smartmeal-opciones'),
    
    # Buscar platos reales por ingredientes del árbol
    path('smartmeal/buscar-platos/', smartmeal_buscar_platos_por_ingredientes, name='smartmeal-buscar-platos'),
    
    # Estructura completa (solo para debugging)
    path('smartmeal/debug/estructura/', smartmeal_estructura_completa, name='smartmeal-debug'),
]
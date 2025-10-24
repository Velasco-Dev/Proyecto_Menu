# 🍽️ SmartMeal - Sistema de Recomendación Inteligente

## 📋 Descripción del Proyecto

**SmartMeal** es una extensión del proyecto de menú existente que implementa un **árbol de decisión** para guiar a los usuarios en la selección de comidas según sus preferencias. El sistema utiliza estructuras de datos no lineales para crear una experiencia interactiva de recomendación culinaria.

## 🏗️ Arquitectura del Sistema

### Estructura de Datos Implementadas

#### 1. **Lista Doblemente Enlazada** (Sistema Original)
- **Archivo**: `algoritmos/listaDoblementeEnlazada.py`
- **Propósito**: Mantener platos ordenados por puntuación
- **Funcionalidad**: Inserción ordenada y navegación bidireccional

#### 2. **Árbol de Decisión** (Sistema Nuevo - SmartMeal)
- **Archivo**: `algoritmos/arbolDecisionSmartMeal.py`
- **Propósito**: Guiar la selección de comidas mediante preguntas
- **Funcionalidad**: Navegación jerárquica e inteligente

### Flujo del Árbol SmartMeal

```
                    🍽️ Inicio
                        │
        ┌───────────────┼───────────────┐
        │               │               │
    🥣 Desayuno    🍛 Almuerzo      🌙 Cena
        │               │               │
    ┌───┴───┐      ┌────┴────┐      ┌───┴───┐
  🍯Dulce 🧂Salado 🍲Trad. 🥗Salud. 🥗Ligera 🍲Completa
    │       │        │       │        │       │
  [Bases] [Bases]  [Prots] [Ings]   [Tipos] [Prots]
    │       │        │       │        │       │
 [Combos][Combos] [Combos]  ✅      [Combos][Combos]
    │       │        │               │       │
   ✅      ✅       ✅              ✅      ✅
```

## 🚀 Endpoints de la API

### Sistema Original (Lista Enlazada)
- `GET /api/platos/` - Listar todos los platos
- `GET /api/ingredientes/` - Listar todos los ingredientes
- `GET /api/platos-ordenados/` - Platos ordenados por puntuación

### Sistema SmartMeal (Árbol de Decisión)
- `GET /api/smartmeal/` - **Iniciar el sistema**
- `GET /api/smartmeal/navegar/{id_nodo}/` - **Navegar a un nodo específico**
- `GET /api/smartmeal/opciones/{id_nodo}/` - **Obtener opciones de un nodo**
- `POST /api/smartmeal/buscar-platos/` - **Buscar platos por ingredientes**
- `GET /api/smartmeal/debug/estructura/` - **Ver estructura completa (debug)**

## 📁 Estructura de Archivos

```
backend/
├── platos/
│   ├── algoritmos/
│   │   ├── listaDoblementeEnlazada.py    # ✅ Original (No modificado)
│   │   └── arbolDecisionSmartMeal.py     # 🆕 Nuevo árbol de decisión
│   ├── models.py                         # ✅ Original (No modificado)
│   ├── views.py                          # 🔄 Extendido con nuevas vistas
│   ├── urls.py                           # 🔄 Extendido con nuevas rutas
│   └── test_smartmeal.py                 # 🆕 Script de pruebas
├── SMARTMEAL_API_DOCS.md                 # 🆕 Documentación completa
└── README_SMARTMEAL.md                   # 🆕 Este archivo
```

## 🎯 Características Principales

### ✅ Mantenimiento del Sistema Original
- **Sin modificaciones**: El código original permanece intacto
- **Compatibilidad completa**: Funciona junto con el sistema existente
- **Mismos modelos Django**: Reutiliza Plato e Ingrediente

### 🆕 Nuevas Funcionalidades
- **Navegación intuitiva**: Sistema de preguntas y respuestas
- **120+ nodos**: Árbol completo con todas las opciones del diagrama
- **Resultados detallados**: Platos con listas de ingredientes específicos
- **Búsqueda inteligente**: Conecta resultados con la base de datos real

### 🏷️ Tipos de Nodos

1. **Nodos de Decisión** (`decision`)
   - Hacen preguntas al usuario
   - Ejemplo: "¿Qué tipo de comida deseas preparar?"

2. **Nodos de Opción** (`opcion`)
   - Representan las elecciones del usuario
   - Ejemplo: "Desayuno", "Dulce", "Avena"

3. **Nodos de Resultado** (`resultado`)
   - Platos finales con ingredientes específicos
   - Ejemplo: "Avena con miel, canela y almendras"

## 🔄 Flujo de Uso

### Ejemplo de Navegación Completa:

```javascript
// 1. Iniciar SmartMeal
GET /api/smartmeal/
→ Pregunta: "¿Qué tipo de comida deseas preparar hoy?"
→ Opciones: [Desayuno, Almuerzo, Cena]

// 2. Usuario elige "Desayuno"
GET /api/smartmeal/navegar/desayuno/
→ Navega automáticamente a la siguiente pregunta

// 3. Pregunta sobre sabor
GET /api/smartmeal/navegar/sabor_desayuno/
→ Pregunta: "¿Qué sabor prefieres para comenzar el día?"
→ Opciones: [Dulce, Salado]

// 4. Usuario elige "Dulce"
GET /api/smartmeal/navegar/desayuno_dulce/
→ Continúa navegando...

// 5. Resultado final
GET /api/smartmeal/navegar/avena_miel_resultado/
→ Plato: "Avena con miel, canela y almendras"
→ Ingredientes: ["avena", "miel", "canela", "almendras"]
→ es_resultado: true
```

### Búsqueda de Platos Reales:

```javascript
// Usar ingredientes del resultado para buscar en BD
POST /api/smartmeal/buscar-platos/
{
  "ingredientes": ["avena", "miel", "canela", "almendras"]
}
→ Retorna platos reales de la base de datos que coincidan
```

## 📊 Estadísticas del Sistema

- **Total de nodos**: 120+ nodos únicos
- **Preguntas de decisión**: ~25 puntos de decisión
- **Platos resultado**: ~50 platos finales únicos
- **Profundidad máxima**: 7 niveles de navegación
- **Categorías principales**: 3 (Desayuno, Almuerzo, Cena)
- **Subcategorías**: 15+ subcategorías
- **Combinaciones únicas**: 50+ combinaciones de ingredientes

## 🧪 Cómo Probar el Sistema

### 1. Prueba Manual de Navegación
```bash
# Iniciar (desde cualquier cliente HTTP)
GET http://localhost:8000/api/smartmeal/

# Navegar a desayuno
GET http://localhost:8000/api/smartmeal/navegar/desayuno/

# Continuar navegando...
GET http://localhost:8000/api/smartmeal/navegar/sabor_desayuno/
```

### 2. Prueba de Búsqueda
```bash
# Buscar platos por ingredientes
POST http://localhost:8000/api/smartmeal/buscar-platos/
Content-Type: application/json

{
  "ingredientes": ["pollo", "arroz", "ajo"]
}
```

### 3. Script de Prueba Interno
```bash
# Si Python está configurado
cd backend/platos/
python test_smartmeal.py
```

## 🎨 Integración con Frontend

### Datos Disponibles para UI:

```javascript
{
  nodo_actual: {
    id_nodo: "inicio",
    titulo: "¿Qué tipo de comida deseas preparar hoy?",
    tipo: "decision",
    descripcion: "Bienvenido a SmartMeal",
    icono: "🍽️",              // ← Para UI visual
    ingredientes: [],
    es_hoja: false
  },
  opciones: [                 // ← Opciones para botones
    {
      id_nodo: "desayuno",
      titulo: "Desayuno",
      icono: "🥣"
    }
  ],
  ruta: ["Pregunta inicial"],  // ← Para breadcrumbs
  es_resultado: false          // ← Para detectar final
}
```

### Sugerencias de UI:
- **Breadcrumbs**: Usar el array `ruta`
- **Botones**: Cada opción con su icono
- **Progreso**: Mostrar nivel de profundidad
- **Resultados**: Destacar cuando `es_resultado` sea `true`

## 🔮 Ventajas del Diseño

### ✅ Escalabilidad
- **Fácil agregar nodos**: Solo modificar el método `construir_arbol()`
- **Flexible**: Puede agregar nuevas categorías de comida
- **Modular**: Cada rama del árbol es independiente

### ✅ Performance
- **Acceso O(1)**: Diccionario de nodos para acceso rápido por ID
- **Sin recursión**: Navegación iterativa eficiente
- **Cacheable**: Respuestas JSON fácilmente cacheables

### ✅ Mantenibilidad
- **Código limpio**: Métodos bien documentados y organizados
- **Separación de responsabilidades**: Lógica separada de la presentación
- **Extensible**: Fácil agregar nuevos tipos de nodos o funcionalidades

## 🚀 Próximos Pasos

### Funcionalidades Sugeridas:
1. **Sistema de Historial**: Recordar navegaciones previas
2. **Filtros Avanzados**: Tiempo de cocción, dificultad, costo
3. **Personalización**: Adaptar preguntas según preferencias del usuario
4. **Analytics**: Rastrear rutas más populares
5. **Recomendaciones ML**: Usar machine learning para mejorar sugerencias

### Mejoras Técnicas:
1. **Cacheo Redis**: Para mejorar performance
2. **Tests Unitarios**: Cobertura completa de pruebas
3. **Validación**: Validar datos de entrada más estrictamente
4. **Logging**: Sistema de logs para debugging
5. **Internacionalización**: Soporte multi-idioma

## 🤝 Contribución

El sistema está diseñado para ser fácilmente extensible. Para agregar nuevos platos o categorías:

1. **Modificar** `_construir_arbol()` en `arbolDecisionSmartMeal.py`
2. **Agregar** nuevos métodos para las ramas específicas
3. **Probar** con el script `test_smartmeal.py`
4. **Documentar** los nuevos endpoints si es necesario

---

**🎉 ¡SmartMeal está listo para usar! Disfruta explorando las deliciosas opciones culinarias que ofrece.**
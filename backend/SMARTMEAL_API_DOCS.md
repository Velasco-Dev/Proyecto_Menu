# SmartMeal - Árbol de Decisión API

## 📖 Descripción General

SmartMeal es un sistema inteligente de recomendación de comidas implementado como un **árbol de decisión**. Guía a los usuarios a través de una serie de preguntas para ayudarles a decidir qué cocinar según sus preferencias.

## 🏗️ Arquitectura del Sistema

### Estructura de Datos
- **NodoArbol**: Cada nodo representa una pregunta, opción o resultado final
- **ArbolDecisionSmartMeal**: Clase principal que maneja toda la navegación
- **Tipos de nodos**:
  - `decision`: Nodos que hacen preguntas al usuario
  - `opcion`: Opciones que el usuario puede elegir
  - `resultado`: Platos finales con ingredientes específicos

### Flujo del Árbol
```
Inicio (¿Qué tipo de comida?)
├── Desayuno
│   ├── Dulce
│   │   ├── Avena → Combinaciones → Resultados
│   │   ├── Yogurt → Combinaciones → Resultados
│   │   └── Frutas → Combinaciones → Resultados
│   └── Salado
│       ├── Huevos → Combinaciones → Resultados
│       ├── Queso/Tofu → Combinaciones → Resultados
│       └── Pollo → Combinaciones → Resultados
├── Almuerzo
│   ├── Tradicional
│   │   ├── Pollo → Combinaciones → Resultados
│   │   ├── Carne → Combinaciones → Resultados
│   │   ├── Pescado → Combinaciones → Resultados
│   │   └── Cerdo → Combinaciones → Resultados
│   └── Saludable
│       └── Ingredientes → Resultados directos
└── Cena
    ├── Ligera
    │   ├── Ensaladas → Combinaciones → Resultados
    │   └── Sopas → Combinaciones → Resultados
    └── Completa
        ├── Pollo → Combinaciones → Resultados
        ├── Pescado → Combinaciones → Resultados
        └── Vegetariana → Combinaciones → Resultados
```

## 🚀 Endpoints de la API

### 1. **Iniciar SmartMeal**
```http
GET /api/smartmeal/
```

**Respuesta:**
```json
{
  "nodo_actual": {
    "id_nodo": "inicio",
    "titulo": "¿Qué tipo de comida deseas preparar hoy?",
    "tipo": "decision",
    "descripcion": "Bienvenido a SmartMeal - Tu asistente culinario inteligente",
    "icono": "🍽️",
    "ingredientes": [],
    "hijos": ["desayuno", "almuerzo", "cena"],
    "es_hoja": false
  },
  "opciones": [
    {
      "id_nodo": "desayuno",
      "titulo": "Desayuno",
      "tipo": "opcion",
      "icono": "🥣"
    },
    {
      "id_nodo": "almuerzo", 
      "titulo": "Almuerzo",
      "tipo": "opcion",
      "icono": "🍛"
    },
    {
      "id_nodo": "cena",
      "titulo": "Cena", 
      "tipo": "opcion",
      "icono": "🌙"
    }
  ],
  "ruta": ["¿Qué tipo de comida deseas preparar hoy?"],
  "es_resultado": false
}
```

### 2. **Navegar a un Nodo**
```http
GET /api/smartmeal/navegar/{id_nodo}/
```

**Ejemplo:** `GET /api/smartmeal/navegar/desayuno/`

**Respuesta:**
```json
{
  "nodo_actual": {
    "id_nodo": "desayuno",
    "titulo": "Desayuno",
    "tipo": "opcion",
    "descripcion": "Comienza tu día con energía",
    "icono": "🥣"
  },
  "opciones": [
    {
      "id_nodo": "sabor_desayuno",
      "titulo": "¿Qué sabor prefieres para comenzar el día?",
      "tipo": "decision",
      "icono": "☀️"
    }
  ],
  "ruta": ["¿Qué tipo de comida deseas preparar hoy?", "Desayuno"],
  "es_resultado": false
}
```

### 3. **Obtener Solo Opciones**
```http
GET /api/smartmeal/opciones/{id_nodo}/
```

**Respuesta:**
```json
{
  "opciones": [
    {
      "id_nodo": "desayuno_dulce",
      "titulo": "Dulce",
      "tipo": "opcion",
      "icono": "🍯"
    },
    {
      "id_nodo": "desayuno_salado", 
      "titulo": "Salado",
      "tipo": "opcion",
      "icono": "🧂"
    }
  ]
}
```

### 4. **Buscar Platos Reales por Ingredientes**
```http
POST /api/smartmeal/buscar-platos/
Content-Type: application/json

{
  "ingredientes": ["pollo", "arroz", "ajo", "cebolla"]
}
```

**Respuesta:**
```json
{
  "ingredientes_buscados": ["pollo", "arroz", "ajo", "cebolla"],
  "total_platos_encontrados": 3,
  "platos": [
    {
      "id": 1,
      "nombre": "Arroz con Pollo",
      "descripcion": "Delicioso arroz con pollo al estilo criollo",
      "imagen": "url_imagen",
      "precio": 15.50,
      "puntuacion": 8,
      "ingredientes": [
        {
          "nombre": "Pollo",
          "icono": "🍗", 
          "puntuacion": 7
        },
        {
          "nombre": "Arroz",
          "icono": "🍚",
          "puntuacion": 6
        }
      ],
      "coincidencias": 4,
      "porcentaje_coincidencia": 100.0
    }
  ]
}
```

### 5. **Debug - Estructura Completa** 
```http
GET /api/smartmeal/debug/estructura/
```
⚠️ **Solo para desarrollo** - Retorna todo el árbol

## 🔄 Flujo de Uso Típico

### Ejemplo de Navegación Completa:

1. **Inicio**: `GET /api/smartmeal/`
2. **Elegir Desayuno**: `GET /api/smartmeal/navegar/desayuno/`
3. **Preguntar sabor**: `GET /api/smartmeal/navegar/sabor_desayuno/`
4. **Elegir Dulce**: `GET /api/smartmeal/navegar/desayuno_dulce/`
5. **Preguntar base**: `GET /api/smartmeal/navegar/base_dulce/`
6. **Elegir Avena**: `GET /api/smartmeal/navegar/avena/`
7. **Preguntar combinación**: `GET /api/smartmeal/navegar/combo_avena/`
8. **Elegir Miel y Canela**: `GET /api/smartmeal/navegar/avena_miel/`
9. **Resultado Final**: `GET /api/smartmeal/navegar/avena_miel_resultado/`

### Resultado Final:
```json
{
  "nodo_actual": {
    "id_nodo": "avena_miel_resultado",
    "titulo": "Avena con miel, canela y almendras",
    "tipo": "resultado",
    "descripcion": "Plato listo para preparar",
    "icono": "✅",
    "ingredientes": ["avena", "miel", "canela", "almendras"],
    "es_hoja": true
  },
  "opciones": [],
  "ruta": ["¿Qué tipo de comida deseas preparar hoy?", "Desayuno", "¿Qué sabor prefieres para comenzar el día?", "Dulce", "¿Cuál será el ingrediente base?", "Avena", "¿Qué ingredientes combinarás con la avena?", "Miel y canela 🍯", "Avena con miel, canela y almendras"],
  "es_resultado": true
}
```

## 💡 Casos de Uso

### Para el Frontend:
1. **Inicialización**: Llamar al endpoint inicial
2. **Navegación**: Usar los IDs de las opciones para navegar
3. **Historial**: Usar la ruta para mostrar el camino recorrido
4. **Resultado**: Detectar cuando `es_resultado` es `true`
5. **Búsqueda**: Usar los ingredientes del resultado para buscar platos reales

### Para Móviles:
- Los iconos emoji facilitan la UI
- Estructura jerárquica clara para navegación
- Respuestas JSON optimizadas

## 🛠️ Integración con Sistema Existente

El árbol SmartMeal **NO interfiere** con el sistema existente:
- ✅ Mantiene la lista doblemente enlazada original
- ✅ Conserva todos los modelos Django existentes
- ✅ Agrega funcionalidad sin modificar código previo
- ✅ Se puede usar junto con el sistema de puntuaciones actual

## 📊 Estadísticas del Árbol

- **Total de nodos**: 120+ nodos
- **Nodos de decisión**: ~25 preguntas
- **Nodos resultado**: ~50 platos únicos
- **Niveles máximos**: 7 niveles de profundidad
- **Categorías principales**: 3 (Desayuno, Almuerzo, Cena)

## 🧪 Testing

### Comandos de prueba:
```bash
# Probar inicio
curl http://localhost:8000/api/smartmeal/

# Probar navegación
curl http://localhost:8000/api/smartmeal/navegar/desayuno/

# Probar búsqueda de platos
curl -X POST http://localhost:8000/api/smartmeal/buscar-platos/ \
  -H "Content-Type: application/json" \
  -d '{"ingredientes": ["pollo", "arroz"]}'
```

## 🚀 Próximas Mejoras

1. **Sistema de Preferencias**: Recordar elecciones del usuario
2. **Machine Learning**: Mejorar recomendaciones basadas en historial
3. **Filtros Adicionales**: Tiempo de cocción, dificultad, costo
4. **Internacionalización**: Soporte para múltiples idiomas
5. **Cacheo**: Optimizar respuestas para mejor performance
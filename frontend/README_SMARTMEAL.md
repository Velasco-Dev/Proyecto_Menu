# 🍽️ Frontend SmartMeal - Guía de Usuario

## 📋 Descripción

El frontend de SmartMeal implementa **dos sistemas complementarios** para la recomendación de comidas:

1. **🍽️ Menú Tradicional** - Sistema original con filtros por ingredientes
2. **🤖 SmartMeal IA** - Nuevo sistema de árbol de decisión interactivo

## 🎯 Dos Enfoques, Un Objetivo

### 🍽️ **Menú Tradicional** (`/menu-tradicional` o `/`)
**¿Cuándo usar?** Cuando ya sabes qué ingredientes quieres usar.

**Características:**
- ✅ Filtros de ingredientes en sidebar
- ✅ Selección manual de ingredientes
- ✅ Búsqueda directa en base de datos
- ✅ Muestra precios, puntuaciones e imágenes reales
- ✅ Perfecto para explorar el menú existente

**Flujo de uso:**
1. Selecciona ingredientes en el panel lateral
2. Presiona "Filtrar"
3. Ve platos que coincidan con tus ingredientes
4. Compra directamente del restaurante

---

### 🤖 **SmartMeal IA** (`/smartmeal`)
**¿Cuándo usar?** Cuando no sabes qué cocinar y quieres que te guíen.

**Características:**
- ✅ Preguntas interactivas paso a paso
- ✅ 120+ combinaciones de platos inteligentes
- ✅ Funciona sin necesidad de base de datos
- ✅ Conecta opcionalmente con menú del restaurante
- ✅ Experiencia visual e intuitiva

**Flujo de uso:**
1. Responde: "¿Qué tipo de comida deseas?" (Desayuno/Almuerzo/Cena)
2. Sigue las preguntas sobre sabores y preferencias
3. Recibe una recomendación específica con ingredientes
4. Opción: Buscar ese plato en el menú del restaurante
5. Opción: Cocinar en casa con la receta dada

## 🏗️ Arquitectura del Frontend

### Estructura de Componentes

```
src/
├── components/
│   ├── Header.jsx              # Navegación entre sistemas
│   └── Filters.jsx             # Filtros para menú tradicional
├── layouts/
│   └── LayoutApp.jsx           # Layout adaptativo según ruta
├── pages/
│   ├── MenuPage.jsx            # Menú tradicional (original)
│   └── MenuPageArbol.jsx       # SmartMeal IA (nuevo)
└── routes/
    └── Routes.jsx              # Configuración de rutas
```

### APIs Utilizadas

#### **MenuPage.jsx** (Sistema Original)
```javascript
const API_URL = "http://localhost:8000/api/platos-ordenados/";
```

#### **MenuPageArbol.jsx** (Sistema SmartMeal)
```javascript
const SMARTMEAL_API_BASE = "http://localhost:8000/api/smartmeal";

// Endpoints disponibles:
GET  /api/smartmeal/                     // Iniciar sistema
GET  /api/smartmeal/navegar/{id}/        // Navegar a nodo específico
POST /api/smartmeal/buscar-platos/       // Buscar platos reales por ingredientes
```

## 🚀 Instalación y Configuración

### Prerequisitos
```bash
# Asegurar que el backend Django esté corriendo
cd backend/
python manage.py runserver  # http://localhost:8000
```

### Configurar Frontend
```bash
# Instalar dependencias
cd frontend/
npm install

# Ejecutar en desarrollo  
npm run dev              # http://localhost:5173
```

### URLs Disponibles
- `http://localhost:5173/` - Menú Tradicional (por defecto)
- `http://localhost:5173/menu-tradicional` - Menú Tradicional
- `http://localhost:5173/smartmeal` - SmartMeal IA

## 🧪 Testing de la Interfaz

### Probar Menú Tradicional
1. Ir a http://localhost:5173/menu-tradicional
2. Seleccionar ingredientes en sidebar
3. Presionar "Filtrar"
4. Verificar que se muestren platos

### Probar SmartMeal
1. Ir a http://localhost:5173/smartmeal
2. Responder preguntas paso a paso
3. Llegar hasta un resultado final
4. Probar "Buscar en Menú del Restaurante"
5. Probar "Nueva Búsqueda"

## 🔄 Flujo de Integración SmartMeal

### Paso 1: Navegación por el Árbol
```javascript
// Usuario navega respondiendo preguntas
GET /api/smartmeal/                          // Inicio
GET /api/smartmeal/navegar/desayuno/         // "Desayuno"  
GET /api/smartmeal/navegar/sabor_desayuno/   // Pregunta sabor
// ... continúa hasta resultado final
```

### Paso 2: Resultado Final
```json
{
  "nodo_actual": {
    "titulo": "Avena con miel, canela y almendras",
    "tipo": "resultado",
    "ingredientes": ["avena", "miel", "canela", "almendras"]
  },
  "es_resultado": true
}
```

### Paso 3: Búsqueda Opcional en BD
```javascript
// Usuario presiona "Buscar en Menú del Restaurante"
POST /api/smartmeal/buscar-platos/
{
  "ingredientes": ["avena", "miel", "canela", "almendras"]
}

// Respuesta: platos reales que coincidan
{
  "platos": [
    {
      "nombre": "Bowl de Avena Premium",
      "precio": 12.50,
      "porcentaje_coincidencia": 100.0
    }
  ]
}
```

## 🎨 Características de la Interfaz

### Navegación Inteligente
- **Header adaptativo**: Cambia según el sistema activo
- **Layout condicional**: Con/sin sidebar según la página
- **Breadcrumbs**: Muestra el camino recorrido en SmartMeal

### Diseño Responsivo
- **Mobile First**: Optimizado para dispositivos móviles
- **Grids adaptativos**: Se ajustan según el tamaño de pantalla
- **Navegación colapsible**: En dispositivos pequeños

### Estados de la Aplicación
- **Loading states**: Indicadores de carga durante navegación
- **Error handling**: Manejo graceful de errores de conexión  
- **Empty states**: Mensajes cuando no hay resultados

## 🎯 Ventajas de Cada Sistema

### 🍽️ Menú Tradicional
| ✅ Ventajas | ❌ Limitaciones |
|-------------|------------------|
| Búsqueda directa y rápida | Requiere conocimiento previo |
| Precios e imágenes reales | Puede abrumar con opciones |
| Perfecto para compras | Depende 100% de la BD |
| Familiar para usuarios | Menos guía al usuario |

### 🤖 SmartMeal IA
| ✅ Ventajas | ❌ Limitaciones |
|-------------|------------------|
| Guía paso a paso | Proceso más largo |
| No requiere conocimiento previo | Menos opciones de personalización |
| Experiencia interactiva | Dependiente de la lógica del árbol |
| Funciona sin BD | Platos generados, no reales |

## 📱 Responsive Design

### Breakpoints
```css
/* Mobile */
@media (max-width: 768px) {
  /* Layout vertical, navegación en stack */
}

/* Tablet */
@media (768px - 1024px) {
  /* Layout híbrido */
}

/* Desktop */
@media (min-width: 1024px) {
  /* Layout completo con sidebar */
}
```

### Componentes Adaptativos
```jsx
// Navegación responsiva
<nav className="flex flex-col sm:flex-row gap-2 sm:gap-4">

// Grid responsivo en opciones  
<div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">

// Layout condicional
<div className="flex flex-col lg:flex-row gap-4">
```

## 🔮 Próximas Mejoras

### Funcionalidades Sugeridas
1. **Historial de navegación**: Botón "Atrás" funcional en SmartMeal
2. **Favoritos**: Guardar platos recomendados favoritos
3. **Personalización**: Recordar preferencias del usuario
4. **Modo offline**: Cachear respuestas del árbol
5. **Animaciones**: Transiciones suaves entre preguntas
6. **Dark mode**: Tema oscuro opcional

### Optimizaciones Técnicas
1. **React Query**: Cacheo inteligente de respuestas API
2. **Lazy loading**: Cargar componentes bajo demanda
3. **PWA**: Convertir en Progressive Web App
4. **Performance**: Memoización de componentes pesados

---

**🎉 ¡Disfruta explorando ambos sistemas! Cada uno tiene su propósito y juntos ofrecen una experiencia completa de recomendación culinaria.**
"""
Módulo de Grafo Bipartito Dirigido para búsqueda de recetas.

Estructura:
- Conjunto 1 (Nodos fuente): INGREDIENTES
- Conjunto 2 (Nodos destino): RECETAS
- Aristas dirigidas: INGREDIENTE --> RECETA

Propósito:
Permite buscar eficientemente qué recetas se pueden preparar con los ingredientes
disponibles, identificar recetas completas, casi completas e incompletas.
"""

from typing import List, Dict, Set, Tuple
from collections import defaultdict, deque


class Vertex:
    """Representa un vértice en el grafo (Ingrediente o Receta)."""
    
    def __init__(self, name: str, vertex_type: str):
        """
        Args:
            name (str): Nombre del vértice (ej: "pollo", "Arroz con pollo")
            vertex_type (str): Tipo del vértice ("ingrediente" o "receta")
        """
        self.name = name
        self.vertex_type = vertex_type  # "ingrediente" o "receta"
    
    def get_name(self) -> str:
        """Retorna el nombre del vértice."""
        return self.name
    
    def get_type(self) -> str:
        """Retorna el tipo del vértice."""
        return self.vertex_type
    
    def __str__(self) -> str:
        return f"{self.name} ({self.vertex_type})"
    
    def __repr__(self) -> str:
        return f"Vertex({self.name}, {self.vertex_type})"
    
    def __hash__(self):
        return hash((self.name, self.vertex_type))
    
    def __eq__(self, other):
        if isinstance(other, Vertex):
            return self.name == other.name and self.vertex_type == other.vertex_type
        return False


class Edge:
    """Representa una arista dirigida en el grafo (Ingrediente --> Receta)."""
    
    def __init__(self, origen: Vertex, destino: Vertex):
        """
        Args:
            origen (Vertex): Vértice de origen (debe ser un ingrediente)
            destino (Vertex): Vértice de destino (debe ser una receta)
        
        Raises:
            ValueError: Si los vértices no son del tipo correcto
        """
        if origen.get_type() != "ingrediente":
            raise ValueError(f"El origen debe ser un ingrediente, no {origen.get_type()}")
        if destino.get_type() != "receta":
            raise ValueError(f"El destino debe ser una receta, no {destino.get_type()}")
        
        self.origen = origen
        self.destino = destino
    
    def get_vi(self) -> Vertex:
        """Retorna el vértice de origen (compatible con código anterior)."""
        return self.origen
    
    def get_vf(self) -> Vertex:
        """Retorna el vértice de destino (compatible con código anterior)."""
        return self.destino
    
    def get_origen(self) -> Vertex:
        """Retorna el vértice de origen."""
        return self.origen
    
    def get_destino(self) -> Vertex:
        """Retorna el vértice de destino."""
        return self.destino
    
    def __str__(self) -> str:
        return f"{self.origen.get_name()} --> {self.destino.get_name()}"
    
    def __repr__(self) -> str:
        return f"Edge({self.origen}, {self.destino})"


class BipartiteDirectedGraph:
    """
    Grafo Bipartito Dirigido: Ingredientes --> Recetas.
    
    Estructura:
    - Nodos 1 (izquierda): INGREDIENTES
    - Nodos 2 (derecha): RECETAS
    - Aristas: Solo de Ingredientes a Recetas (dirigidas, no de vuelta)
    
    Aplicación: Dado un conjunto de ingredientes disponibles,
    encontrar qué recetas puedo hacer (completas), cuáles están casi completas
    (faltando pocos ingredientes) y cuáles no puedo hacer.
    """
    
    def __init__(self):
        """Inicializa el grafo bipartito vacío."""
        # Diccionario de adyacencia: {ingrediente_vertex: [receta_vertex, ...]}
        self.adyacencia = defaultdict(list)
        
        # Conjuntos separados para ingredientes y recetas
        self.ingredientes: Set[Vertex] = set()
        self.recetas: Set[Vertex] = set()
        
        # Inverso: {receta_vertex: [ingrediente_vertex, ...]}
        # Útil para saber qué ingredientes necesita una receta
        self.recetas_ingredientes = defaultdict(list)
    
    def add_vertex(self, vertex: Vertex) -> None:
        """
        Añade un vértice (ingrediente o receta) al grafo.
        
        Args:
            vertex (Vertex): El vértice a añadir
        
        Raises:
            ValueError: Si el vértice no es de tipo válido
        """
        if vertex.get_type() == "ingrediente":
            self.ingredientes.add(vertex)
        elif vertex.get_type() == "receta":
            self.recetas.add(vertex)
        else:
            raise ValueError(f"Tipo de vértice inválido: {vertex.get_type()}")
    
    def add_edge(self, edge: Edge) -> None:
        """
        Añade una arista dirigida Ingrediente --> Receta.
        
        Args:
            edge (Edge): La arista a añadir
        
        Raises:
            ValueError: Si los vértices no están en el grafo
        """
        origen = edge.get_origen()
        destino = edge.get_destino()
        
        if origen not in self.ingredientes:
            raise ValueError(f"Ingrediente {origen.get_name()} no está en el grafo")
        if destino not in self.recetas:
            raise ValueError(f"Receta {destino.get_name()} no está en el grafo")
        
        # Añadir arista: ingrediente --> receta
        self.adyacencia[origen].append(destino)
        
        # Inverso: receta <-- ingrediente (para búsquedas inversas)
        self.recetas_ingredientes[destino].append(origen)
    
    def is_vertex_in(self, vertex: Vertex) -> bool:
        """Verifica si un vértice está en el grafo."""
        return vertex in self.ingredientes or vertex in self.recetas
    
    def get_vertex_by_name(self, name: str, vertex_type: str) -> Vertex:
        """
        Obtiene un vértice por su nombre y tipo.
        
        Args:
            name (str): Nombre del vértice
            vertex_type (str): Tipo ("ingrediente" o "receta")
        
        Returns:
            Vertex: El vértice encontrado
        
        Raises:
            ValueError: Si el vértice no existe
        """
        if vertex_type == "ingrediente":
            for v in self.ingredientes:
                if v.get_name().lower() == name.lower():
                    return v
        elif vertex_type == "receta":
            for v in self.recetas:
                if v.get_name().lower() == name.lower():
                    return v
        
        raise ValueError(f"{vertex_type.capitalize()} '{name}' no encontrado")
    
    def get_vertex(self, vertex_name: str) -> Vertex:
        """
        Obtiene un vértice por su nombre (busca en ambos conjuntos).
        Compatible con código anterior.
        
        Args:
            vertex_name (str): Nombre del vértice
        
        Returns:
            Vertex: El vértice encontrado o None
        """
        # Buscar en ingredientes
        for v in self.ingredientes:
            if v.get_name().lower() == vertex_name.lower():
                return v
        
        # Buscar en recetas
        for v in self.recetas:
            if v.get_name().lower() == vertex_name.lower():
                return v
        
        return None
    
    def get_recetas_por_ingrediente(self, ingrediente: Vertex) -> List[Vertex]:
        """
        Obtiene todas las recetas que contienen un ingrediente específico.
        
        Args:
            ingrediente (Vertex): El ingrediente a buscar
        
        Returns:
            List[Vertex]: Lista de recetas que usan este ingrediente
        """
        return self.adyacencia.get(ingrediente, [])
    
    def get_ingredientes_por_receta(self, receta: Vertex) -> List[Vertex]:
        """
        Obtiene todos los ingredientes que necesita una receta.
        
        Args:
            receta (Vertex): La receta a buscar
        
        Returns:
            List[Vertex]: Lista de ingredientes necesarios
        """
        return self.recetas_ingredientes.get(receta, [])
    
    def get_neighbors(self, vertex: Vertex) -> List[Vertex]:
        """
        Obtiene los vértices vecinos (compatibilidad con código anterior).
        
        Args:
            vertex (Vertex): Vértice origen
        
        Returns:
            List[Vertex]: Lista de vértices conectados
        """
        return self.adyacencia.get(vertex, [])
    
    def buscar_recetas_por_ingredientes(self, 
                                       ingredientes_disponibles: List[str],
                                       umbral_casi_completa: float = 0.75) -> Dict:
        """
        Busca recetas que pueden prepararse con los ingredientes disponibles.
        
        Clasifica las recetas en:
        - COMPLETAS: Todos los ingredientes disponibles (ratio = 1.0)
        - CASI_COMPLETAS: La mayoría de ingredientes disponibles (ratio >= umbral)
        - INCOMPLETAS: Faltan muchos ingredientes (ratio < umbral)
        
        Args:
            ingredientes_disponibles (List[str]): Lista de nombres de ingredientes disponibles
            umbral_casi_completa (float): Umbral para clasificar como "casi completa" (0..1)
        
        Returns:
            Dict: Diccionario con claves 'completas', 'casi_completas', 'incompletas'
                  Cada una contiene lista de recetas con sus detalles
        """
        # Normalizar nombres de ingredientes (minúsculas y sin espacios)
        ingredientes_disponibles_norm = {ing.strip().lower() for ing in ingredientes_disponibles}
        
        print(f"[DEBUG] Ingredientes disponibles normalizados: {ingredientes_disponibles_norm}")
        
        resultados = {
            'completas': [],
            'casi_completas': [],
            'incompletas': []
        }
        
        # Recorrer todas las recetas
        for receta in self.recetas:
            ingredientes_necesarios = self.get_ingredientes_por_receta(receta)
            
            if not ingredientes_necesarios:
                # Receta sin ingredientes (caso raro)
                print(f"[DEBUG] Receta '{receta.get_name()}' sin ingredientes")
                continue
            
            # Contar ingredientes disponibles y faltantes
            ingredientes_faltantes = []
            ingredientes_presentes = 0
            
            for ingrediente in ingredientes_necesarios:
                nombre_ing = ingrediente.get_name().strip().lower()
                if nombre_ing in ingredientes_disponibles_norm:
                    ingredientes_presentes += 1
                else:
                    ingredientes_faltantes.append(ingrediente.get_name())
            
            # Calcular ratio de disponibilidad
            ratio = ingredientes_presentes / len(ingredientes_necesarios)
            
            # Crear resultado parcial
            resultado_receta = {
                'nombre': receta.get_name(),
                'ingredientes_totales': len(ingredientes_necesarios),
                'ingredientes_disponibles': ingredientes_presentes,
                'ingredientes_faltantes': ingredientes_faltantes,
                'cantidad_faltantes': len(ingredientes_faltantes),
                'ratio': round(ratio, 4),
                'score': round(ratio * 100, 2)
            }
            
            print(f"[DEBUG] Receta: {receta.get_name()}, Ratio: {ratio}, Score: {resultado_receta['score']}")
            
            # Clasificar según ratio
            if ratio == 1.0:
                resultados['completas'].append(resultado_receta)
            elif ratio >= umbral_casi_completa:
                resultados['casi_completas'].append(resultado_receta)
            else:
                resultados['incompletas'].append(resultado_receta)
        
        # Ordenar cada categoría por score (descendente)
        for categoria in resultados:
            resultados[categoria].sort(key=lambda x: x['score'], reverse=True)
        
        return resultados
    
    def bfs_recetas_accesibles(self, ingrediente_inicio: Vertex) -> List[Vertex]:
        """
        Búsqueda en anchura (BFS) para encontrar todas las recetas accesibles
        desde un ingrediente específico.
        
        Args:
            ingrediente_inicio (Vertex): Ingrediente de partida
        
        Returns:
            List[Vertex]: Lista de recetas alcanzables desde ese ingrediente
        """
        visitadas = set()
        cola = deque([ingrediente_inicio])
        recetas_alcanzables = []
        
        while cola:
            vertice_actual = cola.popleft()
            
            if vertice_actual in visitadas:
                continue
            
            visitadas.add(vertice_actual)
            
            # Si es una receta, añadirla a resultados
            if vertice_actual.get_type() == "receta":
                recetas_alcanzables.append(vertice_actual)
            else:
                # Si es ingrediente, explorar sus vecinos (recetas)
                vecinos = self.get_recetas_por_ingrediente(vertice_actual)
                cola.extend(vecinos)
        
        return recetas_alcanzables
    
    def __str__(self) -> str:
        """Representación en string del grafo."""
        output = "=== GRAFO BIPARTITO DIRIGIDO ===\n"
        output += f"Ingredientes: {len(self.ingredientes)}\n"
        output += f"Recetas: {len(self.recetas)}\n"
        output += f"Aristas: {sum(len(v) for v in self.adyacencia.values())}\n\n"
        output += "=== ARISTAS (Ingrediente --> Receta) ===\n"
        
        for ingrediente in self.ingredientes:
            recetas = self.get_recetas_por_ingrediente(ingrediente)
            for receta in recetas:
                output += f"{ingrediente.get_name()} --> {receta.get_name()}\n"
        
        return output


def build_graph_desde_db(platos_db: List[Dict]) -> BipartiteDirectedGraph:
    """
    Construye un grafo bipartito dirigido a partir de una base de datos de platos.
    
    Args:
        platos_db (List[Dict]): Lista de diccionarios con estructura:
            {
                'id': 1,
                'nombre': 'Arroz con pollo',
                'ingredientes': ['pollo', 'arroz', 'ajo', 'cebolla', 'aceite']
            }
    
    Returns:
        BipartiteDirectedGraph: El grafo construido
    
    Raises:
        ValueError: Si la base de datos es inválida
    """
    if not isinstance(platos_db, list):
        raise ValueError("platos_db debe ser una lista")
    
    grafo = BipartiteDirectedGraph()
    
    # Conjuntos para evitar duplicados
    ingredientes_añadidos = set()
    recetas_añadidas = set()
    
    print(f"[DEBUG] Construyendo grafo desde {len(platos_db)} platos...")
    
    # Primero, recorrer todos los platos para añadir vértices
    for plato in platos_db:
        nombre_receta = plato.get('nombre', '').strip()
        if not nombre_receta or nombre_receta in recetas_añadidas:
            continue
        
        # Crear vértice de receta
        receta_vertex = Vertex(nombre_receta, "receta")
        grafo.add_vertex(receta_vertex)
        recetas_añadidas.add(nombre_receta)
        
        # Procesar ingredientes de esta receta
        ingredientes = plato.get('ingredientes', [])
        for ing in ingredientes:
            nombre_ing = ing.strip().lower() if isinstance(ing, str) else ""
            
            if not nombre_ing:
                continue
            
            # Crear vértice de ingrediente (si no existe)
            if nombre_ing not in ingredientes_añadidos:
                ingrediente_vertex = Vertex(nombre_ing, "ingrediente")
                grafo.add_vertex(ingrediente_vertex)
                ingredientes_añadidos.add(nombre_ing)
    
    print(f"[DEBUG] Vértices creados: {len(ingredientes_añadidos)} ingredientes, {len(recetas_añadidas)} recetas")
    
    # Segundo, crear las aristas (Ingrediente --> Receta)
    aristas_creadas = 0
    for plato in platos_db:
        nombre_receta = plato.get('nombre', '').strip()
        if not nombre_receta:
            continue
        
        try:
            receta_vertex = grafo.get_vertex_by_name(nombre_receta, "receta")
        except ValueError:
            continue
        
        ingredientes = plato.get('ingredientes', [])
        for ing in ingredientes:
            nombre_ing = ing.strip().lower() if isinstance(ing, str) else ""
            if not nombre_ing:
                continue
            
            try:
                ingrediente_vertex = grafo.get_vertex_by_name(nombre_ing, "ingrediente")
                # Crear arista: ingrediente --> receta
                arista = Edge(ingrediente_vertex, receta_vertex)
                grafo.add_edge(arista)
                aristas_creadas += 1
            except ValueError:
                # Ingrediente no encontrado (no debería ocurrir)
                pass
    
    print(f"[DEBUG] Aristas creadas: {aristas_creadas}")
    
    return grafo

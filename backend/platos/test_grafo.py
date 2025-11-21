

# =====================================================
# EJEMPLO DE USO (para testing local)
# =====================================================

if __name__ == "__main__":
    print("=== TEST 1: Crear grafo manualmente ===\n")
    
    # Crear grafo de ejemplo
    grafo = BipartiteDirectedGraph()
    
    # Crear vértices de ingredientes
    pollo = Vertex("pollo", "ingrediente")
    arroz = Vertex("arroz", "ingrediente")
    ajo = Vertex("ajo", "ingrediente")
    cebolla = Vertex("cebolla", "ingrediente")
    aceite = Vertex("aceite", "ingrediente")
    huevo = Vertex("huevo", "ingrediente")
    leche = Vertex("leche", "ingrediente")
    
    # Crear vértices de recetas
    arroz_con_pollo = Vertex("Arroz con pollo", "receta")
    tortilla = Vertex("Tortilla española", "receta")
    frittata = Vertex("Frittata", "receta")
    
    # Añadir vértices al grafo
    for v in [pollo, arroz, ajo, cebolla, aceite, huevo, leche, arroz_con_pollo, tortilla, frittata]:
        grafo.add_vertex(v)
    
    # Añadir aristas (relaciones ingrediente --> receta)
    grafo.add_edge(Edge(pollo, arroz_con_pollo))
    grafo.add_edge(Edge(arroz, arroz_con_pollo))
    grafo.add_edge(Edge(ajo, arroz_con_pollo))
    grafo.add_edge(Edge(cebolla, arroz_con_pollo))
    grafo.add_edge(Edge(aceite, arroz_con_pollo))
    
    grafo.add_edge(Edge(huevo, tortilla))
    grafo.add_edge(Edge(cebolla, tortilla))
    grafo.add_edge(Edge(aceite, tortilla))
    
    grafo.add_edge(Edge(huevo, frittata))
    grafo.add_edge(Edge(leche, frittata))
    grafo.add_edge(Edge(aceite, frittata))
    
    # Mostrar grafo
    print(grafo)
    
    # Buscar recetas con ingredientes disponibles
    print("\n=== BÚSQUEDA DE RECETAS ===")
    ingredientes_disponibles = ["pollo", "arroz", "ajo", "cebolla", "aceite"]
    resultados = grafo.buscar_recetas_por_ingredientes(ingredientes_disponibles, umbral_casi_completa=0.75)
    
    print(f"\nIngredientes disponibles: {ingredientes_disponibles}\n")
    print(f"RECETAS COMPLETAS ({len(resultados['completas'])}):")
    for r in resultados['completas']:
        print(f"  ✓ {r['nombre']} (Score: {r['score']}%)")
    
    print(f"\nRECETAS CASI COMPLETAS ({len(resultados['casi_completas'])}):")
    for r in resultados['casi_completas']:
        print(f"  ~ {r['nombre']} | Faltantes: {r['ingredientes_faltantes']} (Score: {r['score']}%)")
    
    print(f"\nRECETAS INCOMPLETAS ({len(resultados['incompletas'])}):")
    for r in resultados['incompletas']:
        print(f"  ✗ {r['nombre']} | Faltantes: {r['ingredientes_faltantes']} (Score: {r['score']}%)")
    
    # Test BFS
    print("\n\n=== TEST 2: BFS desde ingrediente ===\n")
    recetas_bfs = grafo.bfs_recetas_accesibles(pollo)
    print(f"Recetas accesibles desde '{pollo.get_name()}':")
    for r in recetas_bfs:
        print(f"  - {r.get_name()}")
    
    # Test con DB simulada
    print("\n\n=== TEST 3: Construir grafo desde BD simulada ===\n")
    platos_simulados = [
        {
            'id': 1,
            'nombre': 'Arroz con pollo',
            'ingredientes': ['pollo', 'arroz', 'ajo', 'cebolla', 'aceite']
        },
        {
            'id': 2,
            'nombre': 'Tortilla española',
            'ingredientes': ['huevo', 'cebolla', 'aceite', 'papa']
        },
        {
            'id': 3,
            'nombre': 'Frittata',
            'ingredientes': ['huevo', 'leche', 'aceite']
        }
    ]
    
    grafo_db = build_graph_desde_db(platos_simulados)
    print(grafo_db)
    
    print("\n--- Búsqueda en grafo construido desde BD ---")
    ingredientes_test = ["huevo", "cebolla", "aceite"]
    resultados_db = grafo_db.buscar_recetas_por_ingredientes(ingredientes_test, umbral_casi_completa=0.6)
    
    print(f"\nIngredientes disponibles: {ingredientes_test}\n")
    print(f"RECETAS COMPLETAS ({len(resultados_db['completas'])}):")
    for r in resultados_db['completas']:
        print(f"  ✓ {r['nombre']} (Score: {r['score']}%)")
    
    print(f"\nRECETAS CASI COMPLETAS ({len(resultados_db['casi_completas'])}):")
    for r in resultados_db['casi_completas']:
        print(f"  ~ {r['nombre']} | Faltantes: {r['ingredientes_faltantes']} (Score: {r['score']}%)")
    
    print(f"\nRECETAS INCOMPLETAS ({len(resultados_db['incompletas'])}):")
    for r in resultados_db['incompletas']:
        print(f"  ✗ {r['nombre']} | Faltantes: {r['ingredientes_faltantes']} (Score: {r['score']}%)")
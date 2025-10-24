"""
Script de prueba para el Árbol de Decisión SmartMeal
===================================================

Este script permite probar el árbol de decisión SmartMeal desde la consola
sin necesidad de levantar el servidor Django.

Uso:
    python test_smartmeal.py
"""

import sys
import os

# Agregar el directorio del proyecto al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from algoritmos.arbolDecisionSmartMeal import ArbolDecisionSmartMeal

def mostrar_nodo(nodo_info):
    """Muestra la información de un nodo de manera amigable."""
    if not nodo_info:
        print("❌ Nodo no encontrado")
        return
    
    nodo = nodo_info['nodo_actual']
    
    print(f"\n{'='*60}")
    print(f"📍 {nodo['icono']} {nodo['titulo']}")
    print(f"{'='*60}")
    
    if nodo['descripcion']:
        print(f"📝 {nodo['descripcion']}")
    
    print(f"🏷️  Tipo: {nodo['tipo']}")
    
    if nodo_info['ruta']:
        print(f"🗺️  Ruta: {' → '.join(nodo_info['ruta'])}")
    
    if nodo_info['es_resultado']:
        print(f"🍽️  PLATO FINAL")
        if nodo['ingredientes']:
            print(f"🥘 Ingredientes: {', '.join(nodo['ingredientes'])}")
    
    if nodo_info['opciones']:
        print(f"\n🎯 Opciones disponibles:")
        for i, opcion in enumerate(nodo_info['opciones'], 1):
            icono = opcion.get('icono', '▫️')
            print(f"  {i}. {icono} {opcion['titulo']} (ID: {opcion['id_nodo']})")
    else:
        print("\n🏁 No hay más opciones disponibles")


def probar_navegacion_interactiva():
    """Permite navegar por el árbol de manera interactiva."""
    
    print("🌟 ¡Bienvenido a SmartMeal - Prueba Interactiva! 🌟")
    print("Escribe 'salir' en cualquier momento para terminar")
    
    arbol = ArbolDecisionSmartMeal()
    nodo_actual = 'inicio'
    
    while True:
        # Mostrar nodo actual
        nodo_info = arbol.navegar_a(nodo_actual)
        mostrar_nodo(nodo_info)
        
        # Si es un resultado final
        if nodo_info and nodo_info['es_resultado']:
            print("\n🎉 ¡Has llegado a un resultado final!")
            respuesta = input("\n¿Quieres empezar de nuevo? (s/n): ").lower()
            if respuesta == 's':
                nodo_actual = 'inicio'
                continue
            else:
                break
        
        # Si no hay opciones
        if not nodo_info or not nodo_info['opciones']:
            print("⚠️ No hay más opciones disponibles")
            break
        
        # Pedir selección del usuario
        try:
            seleccion = input(f"\n👆 Selecciona una opción (1-{len(nodo_info['opciones'])}) o escribe el ID: ").strip()
            
            if seleccion.lower() == 'salir':
                break
            
            # Intentar como número
            try:
                indice = int(seleccion) - 1
                if 0 <= indice < len(nodo_info['opciones']):
                    nodo_actual = nodo_info['opciones'][indice]['id_nodo']
                else:
                    print("❌ Número de opción inválido")
                    continue
            except ValueError:
                # Intentar como ID directo
                if seleccion in [op['id_nodo'] for op in nodo_info['opciones']]:
                    nodo_actual = seleccion
                else:
                    print("❌ ID de nodo inválido")
                    continue
        
        except KeyboardInterrupt:
            print("\n\n👋 ¡Hasta luego!")
            break
    
    print("\n🙏 ¡Gracias por probar SmartMeal!")


def probar_casos_especificos():
    """Prueba casos específicos del árbol."""
    
    print("\n🧪 Ejecutando pruebas específicas...")
    
    arbol = ArbolDecisionSmartMeal()
    
    # Casos de prueba
    casos_prueba = [
        ('inicio', 'Nodo inicial'),
        ('desayuno', 'Opción desayuno'),
        ('sabor_desayuno', 'Pregunta sabor desayuno'),
        ('avena_miel_resultado', 'Resultado final avena con miel'),
        ('nodo_inexistente', 'Nodo que no existe'),
    ]
    
    for id_nodo, descripcion in casos_prueba:
        print(f"\n🔍 Probando: {descripcion}")
        nodo_info = arbol.navegar_a(id_nodo)
        
        if nodo_info:
            nodo = nodo_info['nodo_actual']
            print(f"  ✅ {nodo['titulo']} (Tipo: {nodo['tipo']})")
            print(f"     Opciones: {len(nodo_info['opciones'])}")
            if nodo_info['es_resultado']:
                print(f"     🍽️ Es resultado final con {len(nodo['ingredientes'])} ingredientes")
        else:
            print("  ❌ No encontrado")


def mostrar_estadisticas():
    """Muestra estadísticas del árbol."""
    
    arbol = ArbolDecisionSmartMeal()
    estructura = arbol.obtener_estructura_completa()
    
    print(f"\n📊 Estadísticas del Árbol SmartMeal")
    print(f"{'='*50}")
    print(f"📈 Total de nodos: {estructura['total_nodos']}")
    
    # Contar tipos de nodos
    tipos = {}
    resultados_con_ingredientes = 0
    
    for nodo_dict in estructura['todos_los_nodos'].values():
        tipo = nodo_dict['tipo']
        tipos[tipo] = tipos.get(tipo, 0) + 1
        
        if tipo == 'resultado' and nodo_dict['ingredientes']:
            resultados_con_ingredientes += 1
    
    for tipo, cantidad in tipos.items():
        emoji = {'decision': '❓', 'opcion': '⚡', 'resultado': '🍽️'}
        print(f"{emoji.get(tipo, '📄')} {tipo.title()}: {cantidad}")
    
    print(f"🥘 Platos con ingredientes: {resultados_con_ingredientes}")
    
    # Mostrar algunos ejemplos de resultados
    print(f"\n🍽️ Ejemplos de platos finales:")
    contador = 0
    for nodo_id, nodo_dict in estructura['todos_los_nodos'].items():
        if nodo_dict['tipo'] == 'resultado' and nodo_dict['ingredientes'] and contador < 5:
            ingredientes_str = ', '.join(nodo_dict['ingredientes'][:3])
            if len(nodo_dict['ingredientes']) > 3:
                ingredientes_str += '...'
            print(f"  • {nodo_dict['titulo']}")
            print(f"    Ingredientes: {ingredientes_str}")
            contador += 1


if __name__ == "__main__":
    print("🔬 SmartMeal - Script de Pruebas")
    print("=" * 40)
    
    while True:
        print("\n🎯 ¿Qué quieres hacer?")
        print("1. 🎮 Navegación interactiva")
        print("2. 🧪 Pruebas específicas")
        print("3. 📊 Ver estadísticas")
        print("4. 🚪 Salir")
        
        opcion = input("\nSelecciona una opción (1-4): ").strip()
        
        if opcion == '1':
            probar_navegacion_interactiva()
        elif opcion == '2':
            probar_casos_especificos()
        elif opcion == '3':
            mostrar_estadisticas()
        elif opcion == '4':
            print("👋 ¡Hasta luego!")
            break
        else:
            print("❌ Opción inválida")
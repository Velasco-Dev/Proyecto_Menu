#!/usr/bin/env python3
"""
Script de prueba para verificar la estructura del árbol SmartMeal
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from platos.algoritmos.arbolDecisionSmartMeal import ArbolDecisionSmartMeal

def probar_flujo_desayuno():
    """Prueba el flujo de desayuno según el diagrama"""
    print("🧪 PROBANDO FLUJO DE DESAYUNO SEGÚN DIAGRAMA")
    print("=" * 50)
    
    # Crear el árbol
    arbol = ArbolDecisionSmartMeal()
    
    # 1. Iniciar en la raíz
    print("\n1️⃣ INICIO:")
    inicio = arbol.navegar_a('inicio')
    if inicio:
        print(f"   Pregunta: {inicio['nodo']['titulo']}")
        print(f"   Opciones disponibles: {len(inicio['opciones'])}")
        for opcion in inicio['opciones']:
            print(f"   - {opcion['titulo']} ({opcion['id_nodo']})")
    
    # 2. Seleccionar Desayuno
    print("\n2️⃣ SELECCIONANDO DESAYUNO:")
    desayuno = arbol.navegar_a('desayuno')
    if desayuno:
        print(f"   Pregunta: {desayuno['nodo']['titulo']}")
        print(f"   Descripción: {desayuno['nodo']['descripcion']}")
        print(f"   Icono: {desayuno['nodo']['icono']}")
        print(f"   Opciones disponibles: {len(desayuno['opciones'])}")
        for opcion in desayuno['opciones']:
            print(f"   - {opcion['titulo']} ({opcion['id_nodo']})")
    
    # 3. Verificar que las opciones son Dulce y Salado
    print("\n3️⃣ VERIFICACIÓN:")
    opciones_esperadas = ['desayuno_dulce', 'desayuno_salado']
    opciones_actuales = [op['id_nodo'] for op in desayuno['opciones']]
    
    print(f"   Esperado: {opciones_esperadas}")
    print(f"   Actual: {opciones_actuales}")
    
    if set(opciones_esperadas) == set(opciones_actuales):
        print("   ✅ PERFECTO! El flujo coincide con el diagrama")
    else:
        print("   ❌ ERROR: El flujo no coincide con el diagrama")
    
    return desayuno

def probar_flujo_almuerzo():
    """Prueba el flujo de almuerzo"""
    print("\n\n🧪 PROBANDO FLUJO DE ALMUERZO")
    print("=" * 50)
    
    arbol = ArbolDecisionSmartMeal()
    
    # Seleccionar Almuerzo
    almuerzo = arbol.navegar_a('almuerzo')
    if almuerzo:
        print(f"   Pregunta: {almuerzo['nodo']['titulo']}")
        print(f"   Opciones disponibles: {len(almuerzo['opciones'])}")
        for opcion in almuerzo['opciones']:
            print(f"   - {opcion['titulo']} ({opcion['id_nodo']})")

def probar_flujo_cena():
    """Prueba el flujo de cena"""
    print("\n\n🧪 PROBANDO FLUJO DE CENA")
    print("=" * 50)
    
    arbol = ArbolDecisionSmartMeal()
    
    # Seleccionar Cena
    cena = arbol.navegar_a('cena')
    if cena:
        print(f"   Pregunta: {cena['nodo']['titulo']}")
        print(f"   Opciones disponibles: {len(cena['opciones'])}")
        for opcion in cena['opciones']:
            print(f"   - {opcion['titulo']} ({opcion['id_nodo']})")

if __name__ == "__main__":
    try:
        probar_flujo_desayuno()
        probar_flujo_almuerzo() 
        probar_flujo_cena()
        print("\n\n🎉 TODAS LAS PRUEBAS COMPLETADAS")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()